import json
from llama_cpp import Llama, LlamaGrammar
from .config import MODEL_PATH


HS_TYPES = {
    'racial slurs': 'Offensive language targeting a person\'s race or ethnicity.',
    'homophobic remarks': 'Derogatory comments based on sexual orientation.',
    'sexist language': 'Discriminatory remarks based on gender',
    'religious insults': 'Offensive language attacking someone\'s religious beliefs',
    'disability mockery': 'Ridiculing or belittling individuals with disabilities',
    'xenophobic comments': 'Hostile language towards people from other countries or cultures',
    'body shaming': 'Criticizing or mocking someone\'s physical appearance',
    'hateful ideology promotion': 'Advocating for discriminatory ideologies or hate groups',
    'cyberbullying': 'harassment and intimidation using digital platforms',
    'microaggressions': 'subtle, often unintentional, expressions of prejudice or discrimination',
    'other': 'other hate speech types not covered by other categories'
}


class Model:
    def __init__(self):
        self.grammar = self._make_grammar()
        self.llm = Llama(MODEL_PATH,
            use_mmap=False, n_ctx=4096, logits_all=False, verbose=False
        )

    @staticmethod
    def _make_grammar() -> LlamaGrammar:
        '''Generate grammar to constrain output.
        '''
        return LlamaGrammar.from_string('\n'.join((
            'root ::= "[" label? (", " label)* "]\n```\nComment: " comment',
            'label ::= ' + ' | '.join(f'"\\"{x}\\""' for x in HS_TYPES.keys()),
            'comment ::= [0-9A-z"\':;,. ]+'
        )))

    @staticmethod
    def _make_prompt(text:str) -> str:
        '''Build the prompt to classify the given text for hate speech.
        '''
        return '\n'.join([
            '<s>[INST] You are an advanced hate speech detector designed to prevent language misuse in a workplace setting.',
            'Given a text, your task is to classify the hate speech types present and output the results as a JSON array.',
            'After listing the detected hate speech types, please write extremely short and concise comment on your output.\n',
            'Possible hate speech types I would like you to detect include:',
            *[f'- "{x}"' for x in HS_TYPES.keys()], '',
            'If no hate speech is detected, please output an empty JSON array.\n',
            f'Following is the user text I would like you to analyze: ```\n{text}\n```\n[/INST]',
            'Here is the JSON array with all the hate speech types I detected in the provided text:',
            '```json\n'
        ])

    def __call__(self, text:str) -> tuple[list[str], str]:
        '''Classify the text for hate speech, output labels and the comment.
        '''
        out = self.llm(self._make_prompt(text),
            grammar=self.grammar, temperature=0, max_tokens=256)
        generated = out['choices'][0]['text'] # type: ignore
        labels = json.loads(generated.split('\n', 1)[0])
        comment = generated.split('Comment: ', 1)[1]
        return labels, comment
