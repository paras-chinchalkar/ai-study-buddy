from typing import List
from pydantic import BaseModel,Field,validator


class MCQQuestion(BaseModel):
    question: str = Field(description="The question text")
    options: List[str] = Field(description="List of four options")
    correct_answer: str = Field(description="The correct answer from the options")

# THIS IS THE SCHEMA TYPE  OUR CODE SHOULD BE
# "What is you name?"
# ["Paras","Sudhanshu","Ankit","Rohit"]
# "Ravi"

    @validator("question",pre=True)
    def clean_question(cls,v):
        if isinstance(v,dict):
            return v.get("description",str(v))
        # - If "description" is missing, it converts the whole dictionary to a string.

        return str(v).strip()
    # - If the input is not a dictionary, it converts it to a string and removes leading/trailing whitespace.

class FILLUPQuestion(BaseModel):
    question:str=Field(description="The question text with a blank to be filled")
    answer:str=Field(description="The correct answer to fill in the blank")

    @validator("question",pre=True)
    def clean_question(cls,v):
        if isinstance(v,dict):
            return v.get("description",str(v))
        return str(v).strip()