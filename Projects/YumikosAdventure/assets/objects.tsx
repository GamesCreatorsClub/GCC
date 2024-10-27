<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.11" tiledversion="1.11.0" name="objects" tilewidth="32" tileheight="32" tilecount="128" columns="8">
 <image source="images/objects.png" width="256" height="512"/>
 <tile id="0">
  <properties>
   <property name="name" value="coin"/>
   <property name="on_collision">add_object_to_inventory(obj)
remove_collided_object()
say(&quot;Got one coin&quot;)</property>
  </properties>
 </tile>
 <tile id="2">
  <properties>
   <property name="name" value="portal-blue"/>
  </properties>
 </tile>
 <tile id="4">
  <properties>
   <property name="name" value="portal-green"/>
  </properties>
 </tile>
 <tile id="5">
  <properties>
   <property name="name" value="portal-red"/>
  </properties>
 </tile>
 <tile id="8">
  <properties>
   <property name="name" value="door-up"/>
  </properties>
 </tile>
 <tile id="9">
  <properties>
   <property name="name" value="door-down"/>
  </properties>
 </tile>
 <tile id="10">
  <properties>
   <property name="name" value="door-left"/>
  </properties>
 </tile>
 <tile id="11">
  <properties>
   <property name="name" value="door-right"/>
  </properties>
 </tile>
 <tile id="16">
  <properties>
   <property name="name" value="key"/>
  </properties>
 </tile>
</tileset>
