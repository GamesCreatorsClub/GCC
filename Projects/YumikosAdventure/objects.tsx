<?xml version="1.0" encoding="UTF-8"?>
<tileset name="objects" tilewidth="32" tileheight="32" tilecount="128" columns="8">
 <image source="images/objects.png" width="256" height="512"/>
 <tile id="0">
  <properties>
   <property name="OnCollision">AddCoins(1)
RemoveCollidedObject()</property>
   <property name="name" value="coin"/>
  </properties>
 </tile>
</tileset>
