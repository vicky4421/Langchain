'''
text - notes
 |
quiz

text - model1 - notes
 |               |
model2           |
 |               |
 quiz --------- model3 -------- output
'''

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

model1 = init_chat_model('google_genai:gemini-3.5-flash')
model2 = init_chat_model('google_genai:gemini-3.1-flash-lite')

prompt1 = PromptTemplate(
    template='Generate short and simple notes from following text \n {text}',
    input_variables=['text']
)

prompt2 = PromptTemplate(
    template='Generate 5 short question answers from following text \n {text}',
    input_variables=['text']
)

prompt3 = PromptTemplate(
    template='Merge the provided notes and quiz into single document \n notes -> {notes} and quiz -> {quiz}',
    input_variables=['notes', 'quiz']
)

parser = StrOutputParser()

# create two chains which runs parallely and then merge them into one
# runnable i think like java runnables create child threads and run them parallely where you provide two chains

parallel_chain = RunnableParallel({
    # The keys used in this dictionary should match the input variables of prompt input variables as they are input for next chain
    # chain 1 for notes in dict
    'notes': prompt1 | model1 | parser,

    # chain 2 for quiz
    'quiz': prompt2 | model2 | parser
})

# merge two chains into one and feed it to llm
merged_chain = prompt3 | model1 | parser

# final chain
chain = parallel_chain | merged_chain

text = '''
Support vector machines (SVMs) are a set of supervised learning methods used for classification, regression and outliers detection.

The advantages of support vector machines are:

Effective in high dimensional spaces.

Still effective in cases where number of dimensions is greater than the number of samples.

Uses a subset of training points in the decision function (called support vectors), so it is also memory efficient.

Versatile: different Kernel functions can be specified for the decision function. Common kernels are provided, but it is also possible to specify custom kernels.

The disadvantages of support vector machines include:

If the number of features is much greater than the number of samples, avoid over-fitting in choosing Kernel functions and regularization term is crucial.

SVMs do not directly provide probability estimates, these are calculated using an expensive five-fold cross-validation (see Scores and probabilities, below).

The support vector machines in scikit-learn support both dense (numpy.ndarray and convertible to that by numpy.asarray) and sparse (any scipy.sparse) sample vectors as input. However, to use an SVM to make predictions for sparse data, it must have been fit on such data. For optimal performance, use C-ordered numpy.ndarray (dense) or scipy.sparse.csr_matrix (sparse) with dtype=float64.
'''

result = chain.invoke({
    'text': text
})

print(result)
print('\n')
chain.get_graph().print_ascii()

'''
Output:
# Support Vector Machines (SVM): Study Guide & Quiz

---

## Part 1: Study Notes

### **What is SVM?**
* **Type:** Supervised learning method.
* **Uses:** Classification, regression, and outlier detection.

### **Advantages**
* **High Dimensions:** Highly effective in high-dimensional spaces (even when there are more dimensions/features than samples).
* **Memory Efficient:** Uses only a subset of training points (called *support vectors*) in its decision process.
* **Versatile:** Allows different "Kernel" functions (pre-defined or custom) to fit different types of data.

### **Disadvantages**
* **Overfitting Risk:** If features greatly outnumber samples, it requires careful tuning of Kernels and regularization to avoid overfitting.
* **No Direct Probabilities:** It does not naturally calculate probability estimates (doing so requires slow, expensive calculations).

### **Implementation (scikit-learn)**
* **Input Types:** Supports both **dense** and **sparse** data.
* **Key Rule:** To predict on sparse data, the model *must* be trained on sparse data.
* **Best Performance Formats:**
  * *Dense:* `C-ordered numpy.ndarray`
  * *Sparse:* `scipy.sparse.csr_matrix` with `dtype=float64`

---

## Part 2: Practice Quiz

**1. Question: What are the three primary tasks for which Support Vector Machines (SVMs) are used?**
* **Answer:** SVMs are used for classification, regression, and outlier detection.

**2. Question: Why are SVMs considered memory efficient?**
* **Answer:** They are memory efficient because they use only a subset of training points, known as support vectors, in the decision function.

**3. Question: Can users utilize custom kernels in SVMs?**
* **Answer:** Yes, while common kernels are provided, it is possible to specify custom kernels for the decision function.

**4. Question: What is a major disadvantage of SVMs regarding probability estimates?**
* **Answer:** SVMs do not provide probability estimates directly; they must be calculated using expensive five-fold cross-validation.

**5. Question: What input formats does scikit-learn’s SVM support?**
* **Answer:** It supports both dense (`numpy.ndarray`) and sparse (`scipy.sparse`) sample vectors.


                    +---------------------------+
                    | Parallel<notes,quiz>Input |
                    +---------------------------+
                       ***                   ***
                   ****                         ****
                 **                                 **
    +----------------+                          +----------------+
    | PromptTemplate |                          | PromptTemplate |
    +----------------+                          +----------------+
             *                                           *
             *                                           *
             *                                           *
+------------------------+                  +------------------------+
| ChatGoogleGenerativeAI |                  | ChatGoogleGenerativeAI |
+------------------------+                  +------------------------+
             *                                           *
             *                                           *
             *                                           *
    +-----------------+                         +-----------------+
    | StrOutputParser |                         | StrOutputParser |
    +-----------------+                         +-----------------+
                       ***                   ***
                          ****           ****
                              **       **
                    +----------------------------+
                    | Parallel<notes,quiz>Output |
                    +----------------------------+
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