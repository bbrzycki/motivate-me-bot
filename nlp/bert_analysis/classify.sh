# export BERT_BASE_DIR=./cased_L-12_H-768_A-12
# export TRAINED_CLASSIFIER=./bert_output/model.ckpt-303
export BERT_BASE_DIR=./uncased_L-2_H-128_A-2
export TRAINED_CLASSIFIER=./bert_output/model.ckpt-303


python bert/run_classifier.py \
--task_name=cola \
--do_predict=true \
--data_dir=./data \
--vocab_file=$BERT_BASE_DIR/vocab.txt \
--bert_config_file=$BERT_BASE_DIR/bert_config.json \
--init_checkpoint=$TRAINED_CLASSIFIER \
--max_seq_length=128 \
--output_dir=./bert_output/