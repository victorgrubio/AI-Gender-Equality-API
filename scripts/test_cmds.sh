curl -XGET http://localhost:3000/v1/devices/my_dev/type
curl -XGET http://localhost:3000/v1/devices/my_dev/schema
curl -XGET http://localhost:3000/v1/devices/my_dev/map
curl -g -H 'Content-Type: application/json' -XPOST -d "{\"class_path\":\"visiona_ip.parking_sensor.sensor.sensor.ParkingSensor\",\"id\":9,\"persist\":true}" http://localhost:3000/v1/devices/parking_device/create_sensor
curl -g -H 'Content-Type: application/json' -XPOST -d "{\"class_path\":\"visiona_ip.parking_sensor.sensor.sensor.ParkingSensor\",\"id\":9,\"persist\":true}" http://localhost:3000/v1/devices/parking_device/destroy_sensor
curl -XGET http://localhost:3000/v1/devices/my_dev/listener

#Sensors
#MyStupidSensor
curl -XGET http://localhost:3000/v1/sensors/my_stupid_sensor/my_dev/2/type
curl -XGET http://localhost:3000/v1/sensors/my_stupid_sensor/my_dev/2/schema
curl -XGET http://localhost:3000/v1/sensors/my_stupid_sensor/my_dev/2/listener
#ParkingSensor
curl -XGET http://localhost:3000/v1/visiona-ip/sensors/parking_sensor/parking_device/2/type
curl -XGET http://localhost:3000/v1/visiona-ip/sensors/parking_sensor/parking_device/2/schema
curl -XPUT -d '1,2,3,4,5,6,7,8,9' http://localhost:3000/v1/visiona-ip/sensors/parking_sensor/parking_device/3/state
curl -XGET http://localhost:3000/v1/visiona-ip/sensors/parking_sensor/parking_device/2/zones
curl -XPUT -d @points.csv http://localhost:3000/v1/visiona-ip/sensors/parking_sensor/parking_device/2/zones
curl -XGET http://localhost:3000/v1/visiona-ip/sensors/parking_sensor/parking_device/2/listener


