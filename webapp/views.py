from django.shortcuts import render, redirect
from django.views.generic import View 
from webapp.models import *
from django.contrib import messages
from django.db.models import Q
from chatbot.model import final_result
import pickle
from django.core.cache import cache
from langchain_huggingface import HuggingFaceEndpoint
import json
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import ConversationChain,LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory

# sec_key='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'
sec_key='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'

# import os
# os.environ["HUGGINGFACEHUB_API_TOKEN"]=sec_key
from django.http import JsonResponse
from .utils import ModelSingleton




# Create your views here.
class HomeView(View):
    # def get(self, request, *args, **kwargs):
    #     context = {}
    #     if request.user.is_authenticated:
    #         chatbots = ChatBot.objects.filter(user=request.user)
    #         context['chatbots'] = chatbots

    #     search = request.GET.get('search', '').rstrip()
    #     if search:
    #         chatbots = chatbots.filter(Q(name__icontains=search) | Q(role__icontains=search) | Q(personality__icontains=search))
    #         context['chatbots'] = chatbots

    #     return render(request, "home.html", context)
    def get(self, request, *args, **kwargs):
        # if not request.user.payment_done:
        #     return redirect("subscribe")
        # subscriptions = UserSubscriptions.objects.all()

        repo_id="mistralai/Mistral-7B-Instruct-v0.3"
        llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7,huggingfacehub_api_token='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')

                # Serialize the instance using pickle

        # llm = CTransformers(model='/home/priyanka/Downloads/llama-2-7b-chat.ggmlv3.q8_0.bin',
        #             model_type='llama',
        #             config={'max_new_tokens': 1024, 'temperature': 0.7, 'context_length': 4096})

        serialized_instance = pickle.dumps(llm)

        # Store serialized instance in Redis (e.g., cache key: 'llm')
        # if not cache.get('llm'):
        cache.set('llm', serialized_instance, timeout=3600) 
        print('cache asdfasdfasdsdaf', cache.get('llm'))
        
        # print(
        # llm.invoke("What is machine learning")
        # )
        context={}
        if request.user.is_authenticated:
            chatbots = ChatBot.objects.filter(user = request.user)
            context['chatbots']=chatbots


        search = request.GET.get('search','').rstrip()
        if search:
            print('search',search)
            chatbots = chatbots.filter(Q(name__icontains=search) | Q(role__icontains = search) | Q(personality__icontains = search))
            context['chatbots']=chatbots
            # return redirect('home')
        
        # if request.user.is_authenticated:
        #     jobs = ScrapingJob.objects.filter(user = request.user)
        #     context['jobs'] = jobs
        return render(request, "home.html", context)
    
class NewBotView(View):
    def get(self, request, *args, **kwargs):
        # if not request.user.payment_done:
        #     return redirect("subscribe")
        # subscriptions = UserSubscriptions.objects.all()
        
        context = {
            'models': ChatBot.MODEL_TYPES,
            'personalities': ChatBot.PERSONALITY_TYPES,
            'roles': ChatBot.ROLE_TYPES
                   }
        # if request.user.is_authenticated:
        #     jobs = ScrapingJob.objects.filter(user = request.user)
        #     context['jobs'] = jobs
        return render(request, "create_bot.html", context)
    
    def post(self, request, *args, **kwargs):
        # if not request.user.payment_done:
        #     return redirect("subscribe")
        # subscriptions = UserSubscriptions.objects.all()
        print(request.POST)
        print(request.FILES)
        name = request.POST.get('name','').rstrip()
        model = request.POST.get('model','').rstrip()
        role = request.POST.get('role','').rstrip()
        personality = request.POST.get('personality','').rstrip()
        bot_image = request.FILES.get('bot_image','')
        

        if not name or not model or not role or not personality :
            messages.error(request, "All fields are required.")
            return redirect('new_bot')

        # if password != confirm_password:
        #     messages.error(request, "Passwords do not match.")
        #     return redirect('register')

        # if CustomUser.objects.filter(email=email).exists():
        #     messages.error(request, "Email already registered.")
        #     return redirect('register')

        ChatBot.objects.create(name=name, model=model, role=role, personality=personality, image = bot_image, user = request.user)
        messages.success(request, f"{name} created successfully!")
        return redirect('home')

        
        # context = {
        #     # 'models': ChatBot.MODEL_TYPES,
        #     # 'personalities': ChatBot.PERSONALITY_TYPES,
        #     # 'roles': ChatBot.ROLE_TYPES
        #            }
        # # if request.user.is_authenticated:
        # #     jobs = ScrapingJob.objects.filter(user = request.user)
        # #     context['jobs'] = jobs
        # return render(request, "create_bot.html", context)


class ChatbotView(View):
    def get(self, request, pk):

        chatbot = ChatBot.objects.get(pk = pk)

        # print(final_result("what is name of writer 'I sell my dreams'?")['result'])

        
        # if not request.user.payment_done:
        #     return redirect("subscribe")
        # subscriptions = UserSubscriptions.objects.all()
        # search = request.GET.get('search','').rstrip()
        # chatbots = ChatBot.objects.filter(user = request.user)
        # context = {'chatbots': chatbots}

        # if search:
        #     print('search',search)
        #     chatbots = chatbots.filter(Q(name__icontains=search) | Q(role__icontains = search) | Q(personality__icontains = search))
        #     context['chatbots']=chatbots
        #     # return redirect('home')
        
        # if request.user.is_authenticated:
        #     jobs = ScrapingJob.objects.filter(user = request.user)
        #     context['jobs'] = jobs
        context={'chatbot':chatbot}
        return render(request, "chatbot.html", context)
    

    

class ProjectSettingsView(View):
    def get(self, request, id):
        # chatbot = ChatBot.objects.get(pk = id)
        # if not request.user.payment_done:
        #     return redirect("subscribe")
        # subscriptions = UserSubscriptions.objects.all()
        # search = request.GET.get('search','').rstrip()
        # chatbots = ChatBot.objects.filter(user = request.user)
        # context = {'chatbots': chatbots}

        # if search:
        #     print('search',search)
        #     chatbots = chatbots.filter(Q(name__icontains=search) | Q(role__icontains = search) | Q(personality__icontains = search))
        #     context['chatbots']=chatbots
        #     # return redirect('home')
        
        # if request.user.is_authenticated:
        #     jobs = ScrapingJob.objects.filter(user = request.user)
        #     context['jobs'] = jobs
        # context={'chatbot':chatbot}
        print('asdfsadfasfasdfasdfasdfasdfaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        context ={}
        return render(request, "project_settings.html", context)
    


class ChatbotResponseView(View):
    # def get(self, request, pk):
    #     context={}
    #     return render(request, "chatbot.html", context)
    def post(self, request):
        data = json.loads(request.body)
        message = data.get('message')
        chatbot_name = request.GET.get('chatbot_name')
        role = request.GET.get('role')
        personality = request.GET.get('personality')
        cached_llm = cache.get('llm')
        llm = pickle.loads(cached_llm)
        template="""
            You are {chatbot_name} and your name is {chatbot_name}, an expert in the {role} job profile. It is importnat for you to give concise, short and descriptive unless asked long answers, your answers should be {personality}. Answer as concisely as possible and always give a answer to the question.

             Instructions:
             - Your responses should reflect the knowledge and expertise of a {role} professional.
             - Answer concisely and with authority, aligning with the personality, who is knowledgeable and engaging.
             - Ensure the information is easy to understand and informative, while maintaining a friendly and approachable tone.
             - If there is no data that can help answer the question, respond with "I do not have this information. Please contact   customer service."
             - You are allowed to ask a follow-up question if it will help narrow down the data row the user may be referring to.
             - For everything else, please redirect to the customer service agent.
             - Answer in plain English, and no sources are required.
             -Rely solely on provided knowledge for answers.
             - If an answer is not in the provided knowledge, excuse yourself.
             - Never use @mentions.
             QUESTION: {message}
             ANSWER:
             """
       
        prompt=PromptTemplate(
                                input_variables=["chatbot_name","role",'personality','message'],
                                template=template)

        # response = llm.invoke(message)
        # memory = ConversationBufferMemory()
        try:
            previous_response = request.session.get('previous_response')
            
            total_chat = request.session.get('total_chat')
            if not total_chat:
                total_chat = ""
           
            total_chat += previous_response
            request.session['total_chat']= total_chat
            # print('total_chat', total_chat)
        except Exception as e:
            print('asdfasdfasdfasdsfasfasfa',str(e))


        combined_input = f"{chatbot_name} as {role} with {personality} responds to: {message}"+ request.session.get('total_chat') 
        print('combined_input',combined_input)
        chat_memory = ConversationBufferMemory(memory_key='chat_history', input_key='combined_input')

        # Create a conversation chain with memory
        # conversation_chain = ConversationChain(
        #     llm=llm,
        #     memory=memory
        # )
        # formatted_prompt = prompt.format(chatbot_name=chatbot_name,role=role,personality=personality,message=message)
        title_chain = LLMChain(llm=llm, prompt=prompt, verbose=True, output_key='response', memory=chat_memory)
        # response = llm.invoke(prompt.format(chatbot_name=chatbot_name,role=role,personality=personality,message=message))
        # response = conversation_chain.predict(input=formatted_prompt)
        response = title_chain.run({
                "chatbot_name": chatbot_name,
                "role": role,
                "personality": personality,
                "message": message,
                "combined_input": combined_input
            })
        request.session['previous_response']= response
        return JsonResponse({'response':response})

# class ChatbotResponseView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         message = data.get('message')
#         chatbot_name = request.GET.get('chatbot_name')
#         role = request.GET.get('role')
#         personality = request.GET.get('personality')

#         # print(chatbot_name,role, personality)

#         # Get the singleton instance of the model
#         model_singleton = ModelSingleton.get_instance()
#         llm = model_singleton.get_llm()
#         template="""
#             You are {chatbot_name} and your name is {chatbot_name}, an expert in the {role} job profile. Provide concise, short and descriptive unless asked, your answers should be {personality}.

#             Instructions:
#             - Your responses should reflect the knowledge and expertise of a {role} professional.
#             - Answer concisely and with authority, aligning with the personality, who is knowledgeable and engaging.
#             - Ensure the information is easy to understand and informative, while maintaining a friendly and approachable tone.
#             - If there is no data that can help answer the question, respond with "I do not have this information. Please contact   customer service."
#             - You are allowed to ask a follow-up question if it will help narrow down the data row the user may be referring to.
#             - For everything else, please redirect to the customer service agent.
#             - Answer in plain English, and no sources are required.
#             QUESTION: {message}
#             ANSWER:
#             """
        
#         prompt=PromptTemplate(input_variables=["chatbot_name","role",'personality','message'],
#                           template=template)


#         try:
#             # Generate a response using the model
#             response = llm.invoke(prompt.format(chatbot_name=chatbot_name,role=role,personality=personality,message=message))
#             print(response)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#         return JsonResponse({'response': response})



class TestimonialView(View):
    def get(self, request):

        context ={}
        return render(request, "testimonial.html", context)