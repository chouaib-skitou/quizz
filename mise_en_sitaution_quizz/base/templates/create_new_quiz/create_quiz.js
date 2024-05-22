let quiz = {
    title: '',
    questions: []
};

function createQuiz() {
    const quizTitle = document.getElementById('quizTitle').value;
    
    if (quizTitle.trim() === '') {
        alert('Quiz title cannot be empty');
        return;
    }

    quiz.title = quizTitle;
    document.getElementById('quizTitleDisplay').innerText = `Quiz: ${quiz.title}`;
    document.getElementById('quizForm').style.display = 'none';
    document.getElementById('questionSection').style.display = 'block';
}

function addAnswer() {
    const answerDiv = document.createElement('div');
    const answerInput = document.createElement('input');
    answerInput.type = 'text';
    answerInput.className = 'answer';
    answerInput.placeholder = 'Enter answer option';
    answerDiv.appendChild(answerInput);
    document.getElementById('answers').insertBefore(answerDiv, document.querySelector('#answers button'));
}

function addQuestion() {
    const questionText = document.getElementById('questionText').value;
    const answerElements = document.querySelectorAll('.answer');
    const answers = [];

    answerElements.forEach(answerElement => {
        if (answerElement.value.trim() !== '') {
            answers.push(answerElement.value.trim());
        }
    });

    if (questionText.trim() === '' || answers.length === 0) {
        alert('Question and answers cannot be empty');
        return;
    }

    const question = {
        text: questionText,
        answers: answers
    };

    quiz.questions.push(question);
    displayQuestions();
    document.getElementById('questionText').value = '';
    answerElements.forEach(answerElement => answerElement.value = '');
}

function displayQuestions() {
    const questionsList = document.getElementById('questionsList');
    questionsList.innerHTML = '';

    quiz.questions.forEach((question, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question';
        const questionTitle = document.createElement('h3');
        questionTitle.innerText = `Q${index + 1}: ${question.text}`;
        questionDiv.appendChild(questionTitle);

        const answersList = document.createElement('ul');
        question.answers.forEach(answer => {
            const answerItem = document.createElement('li');
            answerItem.innerText = answer;
            answersList.appendChild(answerItem);
        });

        questionDiv.appendChild(answersList);
        questionsList.appendChild(questionDiv);
    });

    document.getElementById('quizDisplay').style.display = 'block';
}
