import torch
from transformers import AutoModel, AutoTokenizer

# peptide_sequence = "AAA"
# protein_sequence = "MMM"

def get_model_and_tokenizer(model_name="ronig/protein_biencoder"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
    model.eval()
    return model, tokenizer


def get_distance(peptide_sequence, protein_sequence, model, tokenizer):
    encoded_peptide = tokenizer.encode_plus(peptide_sequence, return_tensors='pt')
    encoded_protein = tokenizer.encode_plus(protein_sequence, return_tensors='pt')

    with torch.no_grad():
        peptide_output = model.forward1(encoded_peptide)
        protein_output = model.forward2(encoded_protein)

    return torch.norm(peptide_output - protein_output, p=2).item()


if __name__ == """__main__""":
    peptide_sequence = "AAA"
    protein_sequence = "MMM"
    
    model, tokenizer = get_model_and_tokenizer()
    distance = get_distance(peptide_sequence, protein_sequence, model, tokenizer)
    print(distance)
