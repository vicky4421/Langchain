from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = init_chat_model('google_genai:gemini-3.5-flash')
# Note don't keep space on either side of colon, otherwise langchain split the string and it will throw error

prompt = PromptTemplate(
    template='Generate 5 interesting facts about this {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({'topic': 'AI Firmware'})

print(result)

'''
Output:
    Since you didn't specify a particular AI firmware (such as Apple Intelligence, Tesla FSD, or a specific robotic system), here are **5 fascinating facts about modern AI firmware**—the specialized, low-level software that allows AI models to run directly on microchips and hardware devices (often called "Edge AI" or "TinyML"):

    ### 1. It Can Run AI on Less Memory Than an 80s Floppy Disk
    While massive AI models like ChatGPT require giant data centers with thousands of gigabytes of RAM, modern **TinyML (Tiny Machine Learning) firmware** can run neural networks on microcontrollers with **less than 100 KB of RAM** and power budgets measured in milliwatts. This firmware allows smartwatches, hearing aids, and industrial sensors to perform complex tasks like voice recognition and health monitoring locally, without ever needing an internet connection.

    ### 2. "Neuromorphic" Firmware Mimics the Human Brain's Chemistry
    Traditional computer firmware processes data in binary (0s and 1s) at a constant clock speed. However, firmware designed for **neuromorphic chips** (like Intel's Loihi) mimics biological brains. This firmware only processes data when there is a "spike" in electrical activity, meaning the AI chip remains virtually dormant until it detects a change in its environment. This allows devices to perform AI computations using up to **10,000 times less energy** than traditional processors.

    ### 3. It Enables "Over-the-Air Brain Transplants"
    Because AI firmware decouples the hardware from the AI's cognitive abilities, manufacturers can completely rewrite a machine's capabilities overnight. For example, autonomous vehicles (like Teslas) receive over-the-air (OTA) firmware updates that replace the entire underlying neural network architecture. A car parked in a garage overnight can wake up the next morning with a completely restructured "brain" that perceives the world differently, without changing a single piece of physical hardware.

    ### 4. It Features "Self-Healing" Hardware Reconfiguration
    In extreme environments like deep space or nuclear power plants, radiation can physically damage computer chips (a phenomenon called "bit-flipping"). Advanced aerospace AI firmware is designed to be **self-healing**. If a physical transistor on the chip is destroyed, the AI firmware can instantly detect the failure, recalculate the mathematical weights of its neural network, and reroute the processing pathways around the damaged silicon to keep the system running.

    ### 5. It Operates in "Zero-Latency" Microseconds
    For applications like surgical robotics, high-speed drones, or automotive collision avoidance, sending data to a cloud server takes far too long (usually 50 to 100 milliseconds). Edge AI firmware processes sensor data directly on the device's silicon. It can make critical safety decisions in **microseconds (millionths of a second)**—which is hundreds of times faster than a human brain can register a visual stimulus.

    ***

    *If you had a specific AI firmware in mind (e.g., a specific smartphone OS, a robotic vacuum, or an open-source model), let me know and I can give you facts tailored specifically to that system!*
'''

# visualize chain
chain.get_graph().print_ascii()

'''
      +-------------+
      | PromptInput |
      +-------------+
             *
             *
             *
    +----------------+
    | PromptTemplate |
    +----------------+
             *
             *
             *
+------------------------+
| ChatGoogleGenerativeAI |
+------------------------+
             *
             *
             *
    +-----------------+
    | StrOutputParser |
    +-----------------+
             *
             *
             *
+-----------------------+
| StrOutputParserOutput |
+-----------------------+
'''