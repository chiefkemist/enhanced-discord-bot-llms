#!/usr/bin/env python3
import os

import instructor

from instructor import Instructor, AsyncInstructor
from anthropic import Anthropic, AsyncAnthropic
from groq import Groq, AsyncGroq
from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel, Field

from enum import Enum, auto


class LLMModel(str, Enum):
    Claude3 = "claude-3-opus-20240229"
    GPT4_Omni = "gpt-4o"
    LLAMA3 = "llama3-70b-8192"


def gen_client(model=LLMModel.GPT4_Omni) -> Instructor:
    match model:
        case LLMModel.Claude3:
            client = instructor.from_anthropic(Anthropic())
        case LLMModel.GPT4_Omni:
            client = instructor.patch(OpenAI())
        case LLMModel.LLAMA3:
            client = instructor.patch(Groq())
    return client


def gen_async_client(model=LLMModel.GPT4_Omni) -> AsyncInstructor:
    match model:
        case LLMModel.Claude3:
            client = instructor.from_anthropic(AsyncAnthropic())
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
    nouchi = "Nouchi"
    moore = "Mooré"
    lingala = "Lingala"
    english = "English"
    french = "French"
    creole = "Créole"
    spanish = "Spanish"


class GaouJoke(BaseModel):
    friend_gaou_joke: str = Field(
        ...,
        description="The joke that qualifies the friend as a Gaou. The joke should be light and humorous as well as alternate between Nouchi, Mooré, Lingala, English, French, Créole and Spanish.",
    )
    language: Language


async def streaming_gaou_formula(
    ai_client: AsyncInstructor, gaou_name: str, model=LLMModel.GPT4_Omni
) -> GaouJoke:
    gaou = await ai_client.chat.completions.create(
        model=model,
        temperature=1,  # Go wild with the temperature!!!!
        max_tokens=1024,
        response_model=GaouJoke,
        messages=[
            {
                "role": "system",
                "content": f"""
                The term 'Gaou' is a funny term, used only amongs friends. For example, {gaou_name} is so Gaou!.
                You will assist in qualifying a friend as a Gaou, based on the following criteria:
                - The friend's name
                - Make up a light joke which always ends up qualifying the friend as a Gaou
                - Mix in some humor and sarcasm
                - In a way Gaou means someone who is naive, gullible, or easily fooled but in a friendly way
                - Use different languages out of one of the following: Mooré, English, French, Créole, Spanish etc.
                """,
            },
            {"role": "user", "content": gaou_name},
        ],
    )
    return gaou
