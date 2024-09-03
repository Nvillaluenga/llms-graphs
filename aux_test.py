import sacrebleu


def bleu_evaluation_sacrebleu(reference, hypothesis):
    reference = [reference]  # SacreBLEU expects a list of reference texts
    hypothesis = [hypothesis]
    bleu = sacrebleu.corpus_bleu(hypothesis, [reference])
    return bleu.score / 100


# Example usage:
reference_text = "The cat sat on the mat."
hypothesis_text = "The cat is on the mat."

bleu_score = bleu_evaluation_sacrebleu(reference_text, hypothesis_text)
print("BLEU score (SacreBLEU):", bleu_score)
