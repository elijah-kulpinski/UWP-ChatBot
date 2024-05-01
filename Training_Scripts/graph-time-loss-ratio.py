import pandas as pd
import plotly.express as px

# Initialize lists to store extracted data
configurations = []
final_eval_losses = []
total_training_times = []
batch_sizes = []
gradient_accums = []

# Helper function to extract numeric values from configuration strings
def extract_numbers(s):
    return [int(x) for x in s.split() if x.isdigit()]

# Open and read the file
with open('ChatBot Hyperparameter Tuning.txt', 'r') as file:
    for line in file:
        if line.startswith("Device Batch Size:"):
            config = line.strip()
            configurations.append(config)
            nums = extract_numbers(config)
            batch_sizes.append(nums[0])  # Assuming the first number is the batch size
            gradient_accums.append(nums[1])  # Assuming the second number is the gradient accumulation
        elif "'eval_loss':" in line:  # Evaluation loss
            loss_part = line.split("'eval_loss':")[1].split(',')[0].strip()
            final_eval_losses.append(float(loss_part))
        elif "'train_runtime':" in line:  # Total training time
            time_part = line.split("'train_runtime':")[1].split(',')[0].strip()
            total_training_times.append(float(time_part) / 3600)  # Convert seconds to hours

# Ensure lists are aligned by trimming to the shortest length
min_length = min(len(configurations), len(final_eval_losses), len(total_training_times))
configurations = configurations[:min_length]
final_eval_losses = final_eval_losses[:min_length]
total_training_times = total_training_times[:min_length]
batch_sizes = batch_sizes[:min_length]
gradient_accums = gradient_accums[:min_length]

# Create a DataFrame from the lists
df = pd.DataFrame({
    'Configuration': configurations,
    'Final Eval Loss': final_eval_losses,
    'Total Training Time (hours)': total_training_times,
    'Batch Size': batch_sizes,
    'Gradient Accumulation': gradient_accums
})

# Creating the scatter plot for Total Training Time vs. Final Eval Loss
fig = px.scatter(df, x='Total Training Time (hours)', y='Final Eval Loss',
                 hover_data=['Configuration'],
                 title='Total Training Time vs. Final Evaluation Loss',
                 labels={'Total Training Time (hours)': 'Total Training Time (hours)', 'Final Eval Loss': 'Final Evaluation Loss'})

# Enhancing the layout
fig.update_layout(xaxis_title='Total Training Time (hours)',
                  yaxis_title='Final Evaluation Loss')

fig.show()