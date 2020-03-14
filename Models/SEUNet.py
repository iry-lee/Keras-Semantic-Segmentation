#coding=utf-8
from keras.layers import *
from keras.models import *


def SEModule(input, ratio, out_dim):
    # bs, c, h, w
    x = GlobalAveragePooling2D()(input)
    excitation = Dense(units=out_dim // ratio)(x)
    excitation = Activation('relu')(excitation)
    excitation = Dense(units=out_dim)(excitation)
    excitation = Activation('sigmoid')(excitation)
    excitation = Reshape((1, 1, out_dim))(excitation)
    scale = multiply([input, excitation])
    return scale


def Unet(nClasses, input_height=224, input_width=224):
    inputs = Input(shape=(input_height, input_width, 3))
    conv1 = Conv2D(16,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(inputs)
    conv1 = BatchNormalization()(conv1)

    conv1 = Conv2D(16,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(conv1)
    conv1 = BatchNormalization()(conv1)

    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    conv2 = Conv2D(32,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(pool1)
    conv2 = BatchNormalization()(conv2)

    conv2 = Conv2D(32,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(conv2)
    conv2 = BatchNormalization()(conv2)

    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
    conv3 = Conv2D(64,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(pool2)
    conv3 = BatchNormalization()(conv3)

    conv3 = Conv2D(64,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(conv3)
    conv3 = BatchNormalization()(conv3)

    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
    conv4 = Conv2D(128,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(pool3)
    conv4 = BatchNormalization()(conv4)

    conv4 = Conv2D(128,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(conv4)
    conv4 = BatchNormalization()(conv4)

    pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)

    conv5 = Conv2D(256,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(pool4)
    conv5 = BatchNormalization()(conv5)
    conv5 = Conv2D(256,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(conv5)
    conv5 = BatchNormalization()(conv5)

    up6 = Conv2D(128,
                 2,
                 activation='relu',
                 padding='same',
                 kernel_initializer='he_normal')(UpSampling2D(size=(2,
                                                                    2))(conv5))
    up6 = BatchNormalization()(up6)

    merge6 = concatenate([conv4, up6], axis=3)
    conv6 = Conv2D(128,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(merge6)
    conv6 = BatchNormalization()(conv6)

    conv6 = Conv2D(128,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(conv6)
    conv6 = BatchNormalization()(conv6)

    up7 = Conv2D(64,
                 2,
                 activation='relu',
                 padding='same',
                 kernel_initializer='he_normal')(UpSampling2D(size=(2,
                                                                    2))(conv6))
    up7 = BatchNormalization()(up7)

    merge7 = concatenate([conv3, up7], axis=3)
    conv7 = Conv2D(64,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(merge7)
    conv7 = BatchNormalization()(conv7)

    conv7 = Conv2D(64,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(conv7)
    conv7 = BatchNormalization()(conv7)

    up8 = Conv2D(32,
                 2,
                 activation='relu',
                 padding='same',
                 kernel_initializer='he_normal')(UpSampling2D(size=(2,
                                                                    2))(conv7))
    up8 = BatchNormalization()(up8)

    merge8 = concatenate([conv2, up8], axis=3)
    conv8 = Conv2D(32,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(merge8)
    conv8 = BatchNormalization()(conv8)

    conv8 = Conv2D(32,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(conv8)
    conv8 = BatchNormalization()(conv8)

    up9 = Conv2D(16,
                 2,
                 activation='relu',
                 padding='same',
                 kernel_initializer='he_normal')(UpSampling2D(size=(2,
                                                                    2))(conv8))
    up9 = BatchNormalization()(up9)

    merge9 = concatenate([conv1, up9], axis=3)
    conv9 = Conv2D(16,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(merge9)
    conv9 = BatchNormalization()(conv9)

    conv9 = Conv2D(16,
                   3,
                   activation='relu',
                   padding='same',
                   kernel_initializer='he_normal')(conv9)
    conv9 = BatchNormalization()(conv9)

    conv10 = Conv2D(nClasses, (3, 3), padding='same')(conv9)
    conv10 = BatchNormalization()(conv10)

    outputHeight = Model(inputs, conv10).output_shape[1]
    outputWidth = Model(inputs, conv10).output_shape[2]

    out = (Reshape((outputHeight * outputWidth, nClasses)))(conv10)
    out = Activation('softmax')(out)

    model = Model(input=inputs, output=out)
    model.outputHeight = outputHeight
    model.outputWidth = outputWidth

    return model


def SEUnet(nClasses, input_height=224, input_width=224):
    inputs = Input(shape=(input_height, input_width, 3))
    # encode
    # 224x224
    conv1 = Conv2D(64, (3, 3), padding='same')(inputs)
    conv1 = BatchNormalization()(conv1)
    conv1 = (Activation('relu'))(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    # 112x112
    conv2 = Conv2D(128, (3, 3), padding='same')(pool1)
    conv2 = BatchNormalization()(conv2)
    conv2 = (Activation('relu'))(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    # 56x56
    conv3 = Conv2D(256, (3, 3), padding='same')(pool2)
    conv3 = BatchNormalization()(conv3)
    conv3 = (Activation('relu'))(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

    # 28x28
    conv4 = Conv2D(256, (3, 3), padding='same')(pool3)
    conv4 = BatchNormalization()(conv4)
    conv1 = (Activation('relu'))(conv4)
    pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)

    # 14x14
    o = Conv2D(512, (3, 3), padding='same')(pool4)
    o = BatchNormalization()(o)

    # decode
    o = (UpSampling2D((2, 2)))(o)
    # pool 1
    pool3 = SEModule(pool3, 16, 256)
    o = (concatenate([o, pool3], axis=-1))
    # pool 2
    o = SEModule(o, 16, 256 + 512)
    o = (Conv2D(256, (3, 3), padding='same'))(o)
    o = (BatchNormalization())(o)
    o = (Activation('relu'))(o)

    o = (UpSampling2D((2, 2)))(o)
    # pool 1
    pool2 = SEModule(pool2, 16, 128)
    o = (concatenate([o, pool2], axis=-1))
    # pool 2
    o = SEModule(o, 16, 128 + 256)
    o = (Conv2D(128, (3, 3), padding='same'))(o)
    o = (BatchNormalization())(o)
    o = (Activation('relu'))(o)

    o = (UpSampling2D((2, 2)))(o)
    # pool 1
    pool1 = SEModule(pool1, 8, 64)
    o = (concatenate([o, pool1], axis=-1))
    # pool 2
    o = SEModule(o, 8, 64 + 128)
    o = (Conv2D(64, (3, 3), padding='same'))(o)
    o = (BatchNormalization())(o)
    o = (Activation('relu'))(o)

    o = Conv2D(nClasses, (3, 3), padding='same')(o)

    outputHeight = Model(inputs, o).output_shape[1]
    outputWidth = Model(inputs, o).output_shape[2]

    o = (Reshape((outputHeight * outputWidth, nClasses)))(o)
    o = Activation('softmax')(o)

    model = Model(input=inputs, output=o)
    model.outputHeight = outputHeight
    model.outputWidth = outputWidth

    return model
