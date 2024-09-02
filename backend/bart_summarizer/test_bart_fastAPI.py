import requests

test_text =  """The Boy Who Lived Mr and Mrs Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal, thank you very much. 
            They were the last people you’d expect to be involved in anything strange or mysterious, because they just didn’t hold with such nonsense. Mr Dursley was the director 
            of a firm called Grunnings, which made drills. Mrs Dursley was thin and blonde and had nearly twice the usual amount of neck, which came in very useful as she spent 
            so much of her time craning over garden fences, spying on the neighbours. The Dursleys had a small son called Dudley and in their opinion there was no finer boy anywhere. 
            The Dursleys had everything they wanted, but they also had a secret, and their greatest fear was that somebody would discover it. Mrs Potter was Mrs Dursley’s sister, but 
            they hadn’t met for several years; in fact, Mrs Dursley pretended she didn’t have a sister, because her sister and her good-for-nothing husband were as unDursleyish as it 
            was possible to be. The Dursleys shuddered to think what the neighbours would say if the Potters arrived in the street. The Dursleys knew that the Potters had a small son, too, 
            but they had never even seen him. When Mr and Mrs Dursley woke up on the dull, grey Tuesday our story starts, there was nothing about the cloudy sky outside to suggest that 
            strange and mysterious things would soon be happening all over the country. Mr Dursley hummed as he picked out his most boring tie for work and Mrs Dursley gossiped away 
            happily as she wrestled a screaming Dudley into his high chair. None of them noticed a large tawny owl flutter past the window. “Little tyke,” chortled Mr Dursley as he left 
            the house. He got into his car and backed out of number four’s drive. It was on the corner of the street that he noticed the first sign of something peculiar – a cat reading 
            a map. There was a tabby cat standing on the corner of Privet Drive, but there wasn’t a map in sight. What could he have been thinking of? It must have been a trick of the light. 
            It stared back. As Mr Dursley drove around the corner and up the road, he watched the cat in his mirror. It was now reading the sign that said Privet Drive – no, looking at the 
            sign; cats couldn’t read maps or signs. As he drove towards town he thought of nothing except a large order of drills he was hoping to get that day. But on the edge of town, 
            drills were driven out of his mind by something else. As he sat in the usual morning traffic jam, he couldn’t help noticing that there seemed to be a lot of strangely dressed people 
            about. Mr Dursley couldn’t bear people who dressed in funny clothes – the get-ups you saw on young people! He supposed this was some stupid new fashion. He drummed his fingers on 
            the steering wheel and his eyes fell on a huddle of these weirdos standing quite close by. They were whispering excitedly together. The traffic moved on, and a few minutes later, 
            Mr Dursley arrived in the Grunnings car park, his mind back on drills. Mr Dursley always sat with his back to the window in his office on the ninth floor. If he hadn’t, he might 
            have found it harder to concentrate on drills that morning. Most of them had never seen an owl even at night-time. Mr Dursley, however, had a perfectly normal, owl-free morning. 
            He yelled at five different people. He was in a very good mood until lunch-time, when he thought he’d stretch his legs and walk across the road to buy himself a bun from the 
            baker’s opposite. He’d forgotten all about the people in cloaks until he passed a group of them next to the baker’s. He eyed them angrily as he passed. This lot were whispering 
            excitedly, too, and he couldn’t see a single collecting tin. It was on his way back past them, clutching a large doughnut in a bag, that he caught a few words of what they were 
            saying. “The Potters, that’s right, that’s what I heard –” “– yes, their son, Harry –” Mr Dursley stopped dead. He looked back at the whisperers as if he wanted to say something"""

# Define the URL of the FastAPI endpoint where the BART summarization is implemented
url = "http://127.0.0.1:10000/process/"

# Define the payload with the text to be summarized
payload = {
    "text": test_text
}

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, json=payload, headers=headers)

# Print the response
print("Status Code:", response.status_code)
print("Response Body:", response.json())
