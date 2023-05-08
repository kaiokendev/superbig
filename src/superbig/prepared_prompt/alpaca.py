from ..base import PreparedPrompt
import re

class AlpacaPreparedPrompt(PreparedPrompt):
    """
    Format Alpaca-style prompts
    """
    
    ALPACA_FORMAT_STRING_INSTRUCTION = '### Instruction:\n'
    ALPACA_FORMAT_STRING_INPUT = '### Input:\n'
    ALPACA_FORMAT_STRING_RESPONSE = '### Response:\n'
    ALPACA_FORMAT_DELIMITER = "###"

    def from_prompt(self, prompt: str) -> dict:
        def get_substring_between(source: str, substr1: str, substr2: str):
            match = re.search(fr'({substr1}.+?){substr2}', source, flags=re.DOTALL)
            if match:
                return match.group(1).removeprefix(substr1).removesuffix(substr2)
            return ''
            
        instruction_piece_idx = prompt.find(self.ALPACA_FORMAT_STRING_INSTRUCTION)
        input_piece_idx = prompt.find(self.ALPACA_FORMAT_STRING_INPUT)
        response_piece_idx = prompt.find(self.ALPACA_FORMAT_STRING_RESPONSE)
        
        has_instruction: bool = instruction_piece_idx != -1
        has_input: bool = input_piece_idx != -1
        
        instruction_piece = ''
        input_piece = ''
        response_piece = prompt[response_piece_idx:]
        preprompt_piece = prompt[0:instruction_piece_idx]
        
        if has_instruction:
            instruction_piece = get_substring_between(prompt,self.ALPACA_FORMAT_STRING_INSTRUCTION,self.ALPACA_FORMAT_DELIMITER)
        if has_input:
            input_piece = get_substring_between(prompt,self.ALPACA_FORMAT_STRING_INPUT,self.ALPACA_FORMAT_DELIMITER)
            
        return super().from_prompt(prompt, {
            'preprompt': preprompt_piece,
            'instruction': instruction_piece,
            'input': input_piece,
            'response': response_piece,
            'has_instruction': has_instruction,
            'has_input': has_input
        })
        
    def get_search_strings(self) -> list[str]:
        if len(self.prepared_prompt['input']) > 0:
            return [self.prepared_prompt['input']]
        else:
            return [self.prepared_prompt['instruction']]
        
    def rebuild(self) -> str:
        rebuild_prompt = self.prepared_prompt
        
        if self.injected_prompt is not None:
            rebuild_prompt = self.injected_prompt
            
        final_string = f"{rebuild_prompt['preprompt']}"
        
        if rebuild_prompt['has_instruction']:
            final_string += f"{self.ALPACA_FORMAT_STRING_INSTRUCTION}{rebuild_prompt['instruction']}"
            
        if rebuild_prompt['has_input']:
            final_string += f"{self.ALPACA_FORMAT_STRING_INPUT}{rebuild_prompt['input']}"
            
        final_string += f"{rebuild_prompt['response']}"
        return final_string