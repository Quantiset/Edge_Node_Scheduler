class Request:
    def __init__(self, id, prompt_length, output_length, latency, accuracy):
        self.id = id
        self.prompt_length = prompt_length
        self.output_length = output_length
        self.latency = latency
        self.accuracy = accuracy