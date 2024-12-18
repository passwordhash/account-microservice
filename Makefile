include .env

RSA_KEYS_DIR ?= ./keys
PROTO_DIR = ./proto/account_v1
OUT_DIR = ./src/interfaces/grpc
PROTOC = python3 -m grpc_tools.protoc

#export PYTHONPATH := ./src/interfaces/grpc:$(PYTHONPATH)

all: generate-keys generate-proto

generate-keys:
	@echo "Generating RSA keys..."
	@mkdir -p $(RSA_KEYS_DIR)
	@openssl genrsa -out $(RSA_KEYS_DIR)/private.pem 2048
	@openssl rsa -in $(RSA_KEYS_DIR)/private.pem -pubout -out $(RSA_KEYS_DIR)/public.pem

generate-proto:
	@echo "Generating gRPC and Protobuf code..."
	@mkdir -p $(OUT_DIR)
	$(PROTOC) -Isrc/interfaces/grpc=proto \
		--python_out=./ \
		--grpc_python_out=./ \
		 $(PROTO_DIR)/*.proto
	@echo "Code generated in $(OUT_DIR)"


clean:
	@echo "Cleaning generated files..."
	@rm -rf $(OUT_DIR)
	@echo "Cleaned $(OUT_DIR)"
