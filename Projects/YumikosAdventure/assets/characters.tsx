<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.11" tiledversion="1.11.0" name="characters" tilewidth="32" tileheight="32" tilecount="256" columns="16">
 <image source="images/characters.png" width="512" height="512"/>
 <tile id="0">
  <properties>
   <property name="name" value="yumiko-stand1"/>
  </properties>
 </tile>
 <tile id="16">
  <properties>
   <property name="on_enter" value="say_once(&quot;Want to get out? The others clicked on the fire just outside!&quot;); prevent_moving()"/>
   <property name="player" value="down,1"/>
  </properties>
 </tile>
 <tile id="17">
  <properties>
   <property name="player" value="down,2"/>
  </properties>
 </tile>
 <tile id="18">
  <properties>
   <property name="player" value="down,3"/>
  </properties>
 </tile>
 <tile id="19">
  <properties>
   <property name="player" value="down,4"/>
  </properties>
 </tile>
 <tile id="20">
  <properties>
   <property name="player" value="left,1"/>
  </properties>
 </tile>
 <tile id="21">
  <properties>
   <property name="player" value="left,2"/>
  </properties>
 </tile>
 <tile id="22">
  <properties>
   <property name="player" value="left,3"/>
  </properties>
 </tile>
 <tile id="23">
  <properties>
   <property name="player" value="left,4"/>
  </properties>
 </tile>
 <tile id="24">
  <properties>
   <property name="player" value="up,1"/>
  </properties>
 </tile>
 <tile id="25">
  <properties>
   <property name="player" value="up,2"/>
  </properties>
 </tile>
 <tile id="26">
  <properties>
   <property name="player" value="up,3"/>
  </properties>
 </tile>
 <tile id="27">
  <properties>
   <property name="player" value="up,4"/>
  </properties>
 </tile>
 <tile id="28">
  <properties>
   <property name="player" value="right,1"/>
  </properties>
 </tile>
 <tile id="29">
  <properties>
   <property name="player" value="right,2"/>
  </properties>
 </tile>
 <tile id="30">
  <properties>
   <property name="player" value="right,3"/>
  </properties>
 </tile>
 <tile id="31">
  <properties>
   <property name="player" value="right,4"/>
  </properties>
 </tile>
 <tile id="48">
  <properties>
   <property name="name" value="stone-stand"/>
  </properties>
 </tile>
 <tile id="49">
  <properties>
   <property name="name" value="stone-blink"/>
  </properties>
 </tile>
 <tile id="80">
  <properties>
   <property name="thief" value=""/>
  </properties>
 </tile>
</tileset>
