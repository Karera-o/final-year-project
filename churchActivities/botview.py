# from django.http import JsonResponse, HttpResponse

# import os
# import openai

# def openaiView(request):
    
#     file_path = 'csrdata.txt' 
#     file_path = os.path.join(os.path.dirname(__file__), file_path)
#     global text

#     try:
#         with open(file_path, 'r') as file:
#             text = file.read()
#     except FileNotFoundError:
#             text = "File not found"
            
#     print(text)
#     openai.api_key = "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"
    
#     messages =[{"role":"system", "content": 'You are going to act as my facilitator on research I am doing on AI'},]
#     messages.append(
#     {
#       "role": "user",
#       "content": f'Think about what AI ethics means- what is ethical usage of AI??? How AI is being used around the world in different ways… Make bullet-poing notes and list of all citations/ references'
#     },
#     ),
#     messages.append(
#     {
#       "role": "user",
#       "content": f'Please use IEEE standard form of referencing'
#     },
#     ),
#     messages.append(
#     {
#       "role": "user",
#       "content": f'Try to follow CRAAP test while referencing'
#     },
#     ),
#     response = openai.ChatCompletion.create(
#   model="gpt-4",
#   messages= messages,
#   temperature=1,
#   max_tokens=256,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0
# )
    
#     print(response.choices[0].message.content)
    
    
#     return HttpResponse(response.choices[0].message.content)
    
    