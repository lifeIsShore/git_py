# Vector containing price per square meter for each city
price_per_sqm <- c(8000, 5000, 6000, 7000, 5500, 7800, 9000, 6600,
                   7000, 6000, 5000, 5900, 6100)  # Example prices

# 1. Logarithmic transformation
log_weights <- log(price_per_sqm)

# 2. Min-Max normalization
log_weights_normalized <- (log_weights - min(log_weights)) / (max(log_weights) - min(log_weights))

# Display the results
data.frame(
  City_ID = 1:length(price_per_sqm),
  Price_per_sqm = price_per_sqm,
  Log_Weight = log_weights,
  Normalized_Weight = log_weights_normalized
)

# if 0 is a value of one of city it is not a demonstration of absence, 
# since ML model will interepret that as a weighted city score 