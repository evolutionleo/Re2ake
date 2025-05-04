import logging
import sys
import time

import os
from openai import OpenAI

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")

logging.getLogger("openai").disabled = True
logging.getLogger("httpx").disabled = True

class Answerer:
    def answer(self, question: str, faq: dict) -> tuple[str, bool]:
        """
        Метод для получения ответа на вопрос от chatgpt. Так же может быть такое, что не получается ответить используя имеющийся FAQ.
        :param question: вопрос
        :param faq: база вопрос-ответ в формате {'question': 'answer'}
        :return: Возвращает кортеж из 2 переменных: ответ, который уже можно показывать пользователю и получилось ли с помощью базы получить ответ
        :rtype: tuple
        """
        t = int(time.time_ns() / 1e9)

        logging.debug('[%d]\nMethod: answer\n{\nStart params:\nquestion: %s\nfaq: %s\n}\n', t, question, faq)

        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions='''You are a professional customer support agent. Your task is to respond to the client's message in a clear, polite, and helpful manner. 
            Use the provided FAQ (Frequently Asked Questions) to guide your answers: if a similar question exists,
            adapt the approved response while ensuring it fits the new query. Keep responses concise, friendly, and solution-oriented. 
            Format of my requests:

            Client Message: [The customer's question or request]

            FAQ: [Previous questions and approved answers in dictionary format]
            
            Your response should either:

            1. Match the tone and style of the FAQ, if it exists, or
            2. If the exact question isn't in the FAQ but a similar one is, select the closest answer logically.
            3. If no relevant FAQ exists, respond exactly with the phrase "NO DATA", it's crucial that you must respond exactly these 7 symbols if no relevant FAQ exists. Do not halucinate or make up new answers that don't exist.''',
            input=f'''
            Client Message: [{question}]

            FAQ: [{faq}]
            ''',
        )


        answer = response.output_text
        isSuccess = response.output_text == 'NO DATA'

        logging.debug('[%d]\nMethod: answer\n{\nReturn values:\nanswer: %s\nisSuccess: %s\n}\n', t, answer, isSuccess)

        return answer, isSuccess