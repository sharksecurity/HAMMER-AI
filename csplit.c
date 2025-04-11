#include <stdio.h>
#include <stdlib.h>
#include <fann.h>

// 神经网络结构
static struct fann *ann = NULL;

// 初始化神经网络
void init_neural_network() {
    // 创建神经网络
    unsigned int layers[] = {3, 5, 2}; // 输入层3个神经元，隐藏层5个，输出层2个
    ann = fann_create_standard(3, layers[0], layers[1], layers[2]);
    
    // 设置激活函数
    fann_set_activation_function_hidden(ann, FANN_SIGMOID);
    fann_set_activation_function_output(ann, FANN_SIGMOID);
    
    // 设置网络参数（示例）
    fann_set_learning_rate(ann, 0.7);
    fann_set_training_algorithm(ann, FANN_TRAIN_RPROP);
}

// 分析数据
double analyze(double *data, int length) {
    if (ann == NULL) {
        init_neural_network();
    }
    
    // 准备输入数据
    fann_type *input = (fann_type *)malloc(length * sizeof(fann_type));
    for (int i = 0; i < length; i++) {
        input[i] = (fann_type)data[i];
    }
    
    // 运行神经网络
    fann_type *result = fann_run(ann, input);
    
    // 返回结果
    double ret = (double)result[0];
    free(input);
    free(result);
    
    return ret;
}

// 销毁神经网络
void destroy_neural_network() {
    if (ann != NULL) {
        fann_destroy(ann);
        ann = NULL;
    }
}