#!/usr/bin/env python3
import os

import instructor

from instructor import Instructor, AsyncInstructor
from groq import Groq, AsyncGroq
from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel

from enum import Enum, auto


class LLMModel(str, Enum):
    GPT4_Omni = "gpt-4o"
    LLAMA3 = "llama3-8b-8192"


def gen_client(model=LLMModel.GPT4_Omni) -> Instructor:
    match model:
        case LLMModel.GPT4_Omni:
            client = instructor.patch(OpenAI())
            # client = instructor.from_openai(OpenAI())
        case LLMModel.LLAMA3:
            client = instructor.patch(Groq())
    return client


def gen_async_client(model=LLMModel.GPT4_Omni) -> AsyncInstructor:
    match model:
        case LLMModel.GPT4_Omni:
            client = instructor.patch(AsyncOpenAI())
        case LLMModel.LLAMA3:
            client = instructor.patch(AsyncGroq())
    return client


## Gaou Domain


class UserInfo(BaseModel):
    name: str
    age: int
    is_teenager: bool
    is_intelligent: bool


def usine_de_gaou_creation(
    ai_client: Instructor, parametre: str, model=LLMModel.GPT4_Omni
) -> UserInfo:
    gaou = ai_client.chat.completions.create(
        model=model,
        response_model=UserInfo,
        messages=[{"role": "user", "content": parametre}],
    )
    return gaou


async def streaming_usine_de_gaou_creation(
    ai_client: AsyncInstructor, parametre: str, model=LLMModel.GPT4_Omni
) -> UserInfo:
    gaou = await ai_client.chat.completions.create(
        model=model,
        response_model=UserInfo,
        messages=[
            {
                "role": "system",
                "content": "The user may provide a prompt in their language of choice (such as english, french, creol, spanish etc.), so take that fact into account.",
            },
            {"role": "user", "content": parametre},
        ],
    )
    return gaou
