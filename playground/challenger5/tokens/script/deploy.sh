echo "👉 ENTER CONTRACT NAME: "
read CONTRACT_NAME
stellar keys fund alice --network local
stellar keys fund bob --network local
stellar contract build   
stellar contract deploy \
  --wasm target/wasm32-unknown-unknown/release/$CONTRACT_NAME.wasm \
  --source alice \
  --network local