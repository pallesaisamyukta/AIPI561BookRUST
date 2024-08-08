# Stage 1: Build the Rust application
FROM rust:1.70 as builder

# Set the working directory inside the container
WORKDIR /usr/src/myapp

# Copy the source code into the container
COPY . .

# Build and install the Rust application
RUN cargo install --path .

# Stage 2: Create a minimal final image
FROM debian:bullseye-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    # Add other runtime dependencies if necessary
    && rm -rf /var/lib/apt/lists/*

# Copy the built application from the builder stage
COPY --from=builder /usr/local/cargo/bin/bart_openai /usr/local/bin/bart_openai

COPY src/books /books

# Expose the application port
EXPOSE 3030

# Set the default command to run the application
CMD ["bart_openai"]
