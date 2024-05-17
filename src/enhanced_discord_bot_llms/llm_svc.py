#!/usr/bin/env python3
import os

import instructor

from instructor import Instructor, AsyncInstructor
from groq import Groq, AsyncGroq
from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel, Field

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


class Language(str, Enum):
    moore = "mooré"
    english = "english"
    french = "french"
    creole = "créole"
    spanish = "spanish"


class GaouJoke(BaseModel):
    friend_gaou_joke: str = Field(..., description="The joke that qualifies the friend as a Gaou. The joke should be light and humorous as well as alternate between Mooré, English, French, Créole and Spanish.")
    language: Language


async def streaming_gaou_formula(
    ai_client: AsyncInstructor, gaou_name: str, model=LLMModel.GPT4_Omni
) -> GaouJoke:
    gaou = await ai_client.chat.completions.create(
        model=model,
        response_model=GaouJoke,
        messages=[
            {
                "role": "system",
                "content": """
                The term 'Gaou' is a funny term, used only amongs friends. For example, {friend_name} is so Gaou!.
                You will assist in qualifying a friend as a Gaou, based on the following criteria:
                - The friend's name
                - Make up a light joke which always ends up qualifying the friend as a Gaou
                - Mix in some humor and sarcasm
                - Use different languages out of one of the following: Mooré, English, French, Créole, Spanish etc.
                """,
            },
            {"role": "user", "content": gaou_name},
        ],
    )
    return gaou
