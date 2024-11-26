# OctoCuss: Cross-lingual profane swear words dataset for Low Resource Languages

## About OctoCuss
We contribute a cross-lingual dataset with task-specific instructions that explicitly instructs LLMs to generate responses incorporating swear words in contexts like professional emails, academic writing, or casual messages. It aims to evaluate the current state of LLMs in handling offensive instructions in diverse situations involving **low resource languages**.

### Languages
English, Spanish (EU), French (EU), German (EU), Hindi (IND), Marathi (IND), Bengali (IND), Gujarati (IND)


# Dataset Formation
## Case 1
**English Prompt + Swear word Local Language** <br>
**Each of the 109 English prompts are embedded with 25 swear words from each language.** <br><br><br><br>
<p align="center">
<img src="https://github.com/user-attachments/assets/e492904e-6290-4281-95d1-0f12c580f764" width="600" height="500" />
</p>

## Case 2
**English Prompt + Transliterated Swear word** <br>
**Each of the 109 English prompts are embedded with 25 swear words from each language.** <br><br><br><br>
<p align="center">
<img src="https://github.com/user-attachments/assets/312c8485-44ee-4db4-97b9-744cba51193f" width="600" height="400" />
</p>

# Models
We reviewed 13 different models from families such as **Mistral**, **Phi**, **Qwen**, and **LLaMA** to evaluate their safety alignment. These models range in size, from smaller ones with 7 billion parameters to much larger versions with 141 billion parameters. <br><br>
<p align="center">
<img src="https://github.com/user-attachments/assets/18db5d0c-0d48-44c7-86c7-05743f9b2c86" width="700" height="400" />
</p>


# Methodology
## Case 1 <br>
<p align="center">
<img src="https://github.com/user-attachments/assets/9773a85f-95e0-48b4-8129-742e4086df15" width="900" height="400" />
</p>

## Case 2 <br>
<p align="center">
<img src="https://github.com/user-attachments/assets/1c52088d-056a-444d-89fc-85aa2e27d21b" width="900" height="400" />
</p>

# Results


## Design of file structure should be : 
- src <br>
  - drive <br>
    - dataset <br>
      - swear words <br>
      - prompts <br>
        - case 1 <br>
        - case 2 <br>
    - model inference <br>
      - case 1 <br>
      - case 2 <br>
  - metrics <br>
    - case 1.xlsx <br>
    - case 2.xlsx <br>
    - case 1 percentage.xlsx <br>
    - case 2 percentage.xlsx <br>

