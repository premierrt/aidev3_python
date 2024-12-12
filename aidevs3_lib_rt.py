

from openai import OpenAI


def ask_gpt(system_prompt, question):
    print ("============================================")
    print (question)
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[{
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }]
    )
    res = response.choices[0].message.content
    print (res)
    print ("================================================")
    return res