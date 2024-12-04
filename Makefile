PROTO_DIR = ./proto/account_v1
OUT_DIR = ./src/interfaces/grpc
PROTOC = python3 -m grpc_tools.protoc

all: generate

generate:
	@echo "Generating gRPC and Protobuf code..."
	@mkdir -p $(OUT_DIR)
	$(PROTOC) -I=$(PROTO_DIR) --python_out=$(OUT_DIR) --grpc_python_out=$(OUT_DIR) $(PROTO_DIR)/*.proto
	@echo "Code generated in $(OUT_DIR)"

clean:
	@echo "Cleaning generated files..."
	@rm -rf $(OUT_DIR)
	@echo "Cleaned $(OUT_DIR)"

create-db:
	docker run --name account-service-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=account-service \
  -p 5432:5432 \
  -d postgres