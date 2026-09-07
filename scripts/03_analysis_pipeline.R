# ==============================================================================
# Project: Beyond Proficiency: Unpacking Cognitive Engagement with GenAI
# Script: 03_analysis_pipeline.R
# Purpose: Replication of Linear Mixed-Effects Models (LMM) and Data Visualization
# ==============================================================================

# 1. Load Necessary Libraries -------------------------------------------------
if (!require("pacman")) install.packages("pacman")
pacman::p_load(
  tidyverse,  # Data manipulation and ggplot2
  lme4,       # Linear mixed-effects models
  lmerTest,   # P-values for lme4
  emmeans,    # Estimated marginal means for interaction interpretation
  performance,# Model diagnostics (R2, residuals)
  sjPlot,     # Publication-quality tables
  ggpubr      # Plotting enhancements
)

# 2. Load Data ----------------------------------------------------------------
# Assuming the script is run from the /scripts/ directory
data_path <- "../data/survey_long_format.csv"

if (!file.exists(data_path)) {
  stop("Error: survey_long_format.csv not found in ../data/ folder.")
}

df <- read.csv(data_path, stringsAsFactors = TRUE)

# Ensure factors are correctly leveled for the model
# Order: Pre-writing < Drafting < Editing
df$Stage <- factor(df$Stage, levels = c("Pre-writing", "Drafting", "Editing"))

# Order: Beginner < Intermediate < Upper-Intermediate < Advanced (as per your data)
df$Proficiency <- factor(df$Proficiency, levels = c("Beginner", "Intermediate", "Upper-Intermediate", "Advanced"))

# 3. Linear Mixed-Effects Modeling (LMM) ---------------------------------------
cat("\n--- Running Linear Mixed-Effects Model ---\n")

# Model: Engagement Score ~ Proficiency * Stage * Strand + (1 | ParticipantID)
# This matches your reported N=900 model
lmm_model <- lmer(
  Score ~ Proficiency * Stage * Strand + (1 | ParticipantID), 
  data = df
)

# Summary of the model (Fixed effects and P-values)
model_summary <- summary(lmm_model)
print(model_summary)

# 4. Post-hoc Analysis: Interactions -------------------------------------------
cat("\n--- Running Post-hoc Analysis for Significant Interactions ---\n")

# Since you found a significant Intermediate x Editing interaction:
# We use emmeans to probe the interaction
interactions <- emmeans(lmm_model, ~ Proficiency | Stage)
print(interactions)

# Specific probe for the Editing stage across Proficiency levels
editing_probe <- emmeans(lmm_model, pairwise ~ Proficiency | Stage, at = list(Stage = "Editing"))
print(editing_probe$contrasts)

# 5. Model Diagnostics & Fit -------------------------------------------------
cat("\n--- Model Diagnostics and Fit ---\n")

# Check R2 (Marginal and Conditional)
cat("R2 Values:\n")
print(performance::r2(lmm_model))

# Check Residuals (Visual inspection)
# Note: In a real repo, we save these to the output/figures/ folder
plot(lmm_model, main = "Residuals vs Fitted")

# 6. Data Visualization -------------------------------------------------------
cat("\n--- Generating Publication-Quality Plots ---\n")

# Plot 1: Interaction Profile (Cognitive Strand by Stage and Proficiency)
# This recreates the trend lines seen in your paper
p1 <- ggplot(df, aes(x = Stage, y = Score, color = Proficiency, group = Proficiency)) +
  stat_summary(fun = mean, geom = "line", size = 1) +
  stat_summary(fun = mean, geom = "point", size = 3) +
  facet_wrap(~Strand) +
  theme_minimal() +
  labs(
    title = "Cognitive Engagement Trends Across Writing Stages",
    subtitle = "Faceted by Cognitive Strand",
    x = "Writing Stage",
    y = "Mean Engagement Score",
    color = "Proficiency Level"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Save the plot
if (!dir.exists("../output/figures")) dir.create("../output/figures", recursive = TRUE)
ggsave("../output/figures/interaction_profiles.png", p1, width = 12, height = 8, dpi = 300)

# 7. Export Results -----------------------------------------------------------
cat("\n--- Exporting Tables ---\n")

# Export fixed effects table to CSV for easy access
write.csv(as.data.frame(coef(model_summary)$coefficients), 
          "../output/tables/lmm_fixed_effects.csv")

cat("\n[SUCCESS] Analysis complete. Results saved in /output/\n")
