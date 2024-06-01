from openai import OpenAI
import json


api_key = ''
summary_assistant_id = ''


def run_summary(contents):

  summary = ''
  
  client = OpenAI(api_key=api_key)


  thread = client.beta.threads.create()

  message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role='user',
      content=contents
  )

  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=summary_assistant_id
  )

  run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )


  while True:
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )
    
    if run.status != 'in_progress':
      
      if run.status == 'completed':

        messages = client.beta.threads.messages.list(
          thread_id=thread.id
        )
        
        summary = messages.data[0].content[0].text.value
        
        client.beta.threads.delete(thread_id=thread.id)
        
        break
      
      else:
        
        # print(run)
        
        summary = ''
        
        break
  
  
  json_data = {'summary': summary}
  
  return json.dumps(json_data, ensure_ascii=False)
