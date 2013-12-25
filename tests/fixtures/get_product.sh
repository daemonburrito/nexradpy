#!/usr/bin/env bash
# get the sn.last from a station
station=$1
product=$2

usage () {
    echo "usage: get_product.sh \$station \$product"
    echo "example: get_product.sh kewx p94r0"
}

if [ -z $station -o -z $product ] ; then
    usage
    exit 1
fi

echo "Downloading $product from $station."
wget -O "$product-$station.bin" http://weather.noaa.gov/pub/SL.us008001/DF.of/DC.radar/DS.$product/SI.$station/sn.last
