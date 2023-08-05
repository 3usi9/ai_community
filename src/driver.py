from api_readbot import ReadBot
from api_openai import OpenAIBot
def GetDriver(arch, username):
    if(arch == 'readbot'):
        return ReadBot(username=username)
    if(arch == 'gpt-4'):
        return OpenAIBot(username=username, model='gpt-4')
    if(arch == 'gpt-3.5-turbo'):
        return OpenAIBot(username=username, model='gpt-3.5-turbo')
    raise AssertionError(f"Architecture {arch} is not implemented.")