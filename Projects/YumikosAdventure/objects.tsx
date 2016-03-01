<?xml version="1.0" encoding="UTF-8"?>
<tileset name="objects" tilewidth="32" tileheight="32">
 <image source="images/objects.png" width="256" height="512"/>
 <tile id="0">
  <properties>
   <property name="OnCollision">AddCoins(1)
RemoveCollidedObject(); Say(&quot;Got one coin&quot;)</property>
   <property name="name" value="coin"/>
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
   <property name="Name" value="door-up"/>
  </properties>
 </tile>
 <tile id="9">
  <properties>
   <property name="Name" value="door-down"/>
  </properties>
 </tile>
 <tile id="10">
  <properties>
   <property name="Name" value="door-left"/>
  </properties>
 </tile>
 <tile id="11">
  <properties>
   <property name="Name" value="door-right"/>
  </properties>
 </tile>
</tileset>
