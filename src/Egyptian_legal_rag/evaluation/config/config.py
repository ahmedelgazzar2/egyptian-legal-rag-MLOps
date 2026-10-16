configs = [
    {
        "chunk_size": "full_article",
        "overlap": 0,
        "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "k": 3,
    },
    {
        "chunk_size": "full_article",
        "overlap": 0,
        "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "k": 5,
    },
    {
        "chunk_size": "full_article",
        "overlap": 0,
        "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "k": 7,
    },
    {
        "chunk_size": "full_article",
        "overlap": 0,
        "embedding_model": "minishlab/potion-multilingual-128M",
        "k": 3,
    },
    {
        "chunk_size": "full_article",
        "overlap": 0,
        "embedding_model": "minishlab/potion-multilingual-128M",
        "k": 5,
    },
]


ground_truth = [
    {
        "question": "What are the conditions of a valid contract?",
        "ground_truth": "A contract requires offer, acceptance, and legal capacity.",
    },
    {
        "question": "What is the statute of limitations?",
        "ground_truth": "The general statute of limitations is 15 years.",
    },
    {
        "question": "What is force majeure?",
        "ground_truth": "Force majeure is an unforeseeable event preventing contract performance.",
    },
    {
        "question": "What are property ownership rights?",
        "ground_truth": "The owner has the right to use, enjoy and dispose of property.",
    },
    {
        "question": "What is contractual liability?",
        "ground_truth": "Contractual liability arises from breach of contract obligations.",
    },
    {
        "question": "What happens when a contract is void?",
        "ground_truth": "A void contract has no legal effect from the beginning.",
    },
    {
        "question": "What is legal domicile?",
        "ground_truth": "Legal domicile is the place where a person habitually resides.",
    },
    {
        "question": "What is good faith in contracts?",
        "ground_truth": "Good faith requires honest and fair dealing in contract performance.",
    },
    {
        "question": "What is the age of legal capacity?",
        "ground_truth": "Full legal capacity is attained at the age of 21.",
    },
    {
        "question": "What is the definition of obligation?",
        "ground_truth": "An obligation is a legal bond requiring performance of an act.",
    },
    {
        "question": "ما هي شروط صحة العقد؟",
        "ground_truth": "يشترط في العقد الأهلية والتراضي والمحل والسبب.",
    },
    {
        "question": "ما هي مدة التقادم؟",
        "ground_truth": "مدة التقادم خمس عشرة سنة فيما لم يرد فيه نص خاص.",
    },
    {
        "question": "ما هو حق الانتفاع؟",
        "ground_truth": "حق الانتفاع هو حق استعمال الشيء والتمتع بثماره.",
    },
    {
        "question": "ما هي أسباب انقضاء الالتزام؟",
        "ground_truth": "ينقضي الالتزام بالوفاء والتقادم والإبراء والاتحاد الذمة.",
    },
    {
        "question": "ما هو الموطن القانوني؟",
        "ground_truth": "الموطن هو المكان الذي يقيم فيه الشخص عادة.",
    },
    {
        "question": "ما هي شروط التعويض عن الضرر؟",
        "ground_truth": "يشترط لاستحقاق التعويض وجود خطأ وضرر وعلاقة سببية.",
    },
    {
        "question": "ما هو عقد الإيجار؟",
        "ground_truth": "الإيجار عقد يلتزم فيه المؤجر بتمكين المستأجر من الانتفاع بالشيء.",
    },
    {
        "question": "ما هي شروط الهبة؟",
        "ground_truth": "الهبة عقد يتنازل به الواهب عن شيء بغير عوض.",
    },
    {
        "question": "ما هو عقد البيع؟",
        "ground_truth": "البيع عقد يلتزم فيه البائع بنقل الملكية مقابل ثمن.",
    },
    {
        "question": "ما هي شروط الحيازة؟",
        "ground_truth": "الحيازة وضع مادي يباشر فيه الشخص سلطة فعلية على الشيء.",
    },
]


eval_data = [
    {
        "question": "ما هو حكم العقد الباطل في القانون المدني المصري؟",
        "answer": "العقد الباطل هو ما لا أصل له ولا يترتب عليه أثر، ويجوز لكل ذي مصلحة أن يتمسك ببالطلان.",
        "contexts": [
            "مادة 141: إذا كان العقد باطلاً جاز لكل ذي مصلحة أن يتمسك بالبطلان، وللقاضي أن يبرزه من تلقاء نفسه."
        ],
        "ground_truth": "يجوز لكل ذي مصلحة التمسك ببطلان العقد الباطل وللقاضي إبرازه.",
    },
    {
        "question": "متى يسقط الحق بالتقادم في الالتزامات التعاقدية؟",
        "answer": "تسقط الالتزامات التعاقدية بمرور خمس عشرة سنة ما لم ينص القانون على غير ذلك.",
        "contexts": [
            "مادة 374: يتقادم الالتزام بانقضاء خمس عشرة سنة إلا فيما استثناه القانون بنص خاص."
        ],
        "ground_truth": "التقادم العام للالتزامات هو خمس عشرة سنة ما لم يوجد نص خاص.",
    },
]
