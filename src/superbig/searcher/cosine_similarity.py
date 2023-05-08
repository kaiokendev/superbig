import hnswlib
from ..base import Embedding, SearchResult, Searcher

# https://github.com/nmslib/hnswlib
# ef_construction - controls index search speed/build speed tradeoff
#
# M - is tightly connected with internal dimensionality of the data. Strongly affects memory consumption (~M)
# Higher M leads to higher accuracy/run_time at fixed ef/efConstruction
class CosineSimilaritySearcher(Searcher):
    def search(self, query: list[str] | list[Embedding], over_input: list[str] | list[Embedding], k = 1) -> list[SearchResult]:
        index = hnswlib.Index(space = 'cosine', dim = len(over_input[0]))
        index.init_index(max_elements = len(over_input), ef_construction = 200, M = 8)
        index.add_items(over_input, range(len(over_input)))
        index.set_ef(50)
        labels, _ = index.knn_query(query, k = k)
        results = [SearchResult(int(i)) for i in labels[0]]
        del index
        return results