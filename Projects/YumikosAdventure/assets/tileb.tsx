<?xml version="1.0" encoding="UTF-8"?>
<tileset name="tileb" tilewidth="32" tileheight="32" tilecount="256" columns="16">
 <image source="maps/tileb.png" width="512" height="512"/>
 <terraintypes>
  <terrain name="mound" tile="-1"/>
 </terraintypes>
 <tile id="40">
  <properties>
   <property name="name" value="chest-closed"/>
  </properties>
 </tile>
 <tile id="41">
  <properties>
   <property name="name" value="chest-open"/>
  </properties>
 </tile>
 <tile id="44">
  <objectgroup draworder="index">
   <object id="0" x="2.96077" y="1.94301" width="26.832" height="26.3694">
    <ellipse/>
   </object>
  </objectgroup>
 </tile>
 <tile id="81">
  <properties>
   <property name="name" value="sign"/>
  </properties>
  <objectgroup draworder="index">
   <object id="0" x="0.803588" y="13.0766" width="30.8286" height="10.5928"/>
   <object id="0" x="13.0035" y="24.2538" width="5.84428" height="7.52451"/>
  </objectgroup>
 </tile>
 <tile id="230">
  <properties>
   <property name="name" value="plants-killer-1"/>
  </properties>
 </tile>
 <tile id="246">
  <properties>
   <property name="name" value="plants-killer-2"/>
  </properties>
 </tile>
 <tile id="219" terrain=",,,0"/>
 <tile id="220" terrain=",,0,0"/>
 <tile id="221" terrain=",,0,"/>
 <tile id="235" terrain=",0,,0"/>
 <tile id="236" terrain="0,0,0,0"/>
 <tile id="237" terrain="0,,0,"/>
 <tile id="238" terrain=",0,0,0"/>
 <tile id="239" terrain="0,,0,0"/>
 <tile id="251" terrain=",0,,"/>
 <tile id="252" terrain="0,0,,"/>
 <tile id="253" terrain="0,,,"/>
 <tile id="254" terrain="0,0,,0"/>
 <tile id="255" terrain="0,0,0,"/>
<wangsets>
  <wangset name="Terrains" type="corner" tile="-1">
   <wangcolor name="mound" color="#ff0000" tile="-1" probability="1"/>
   <wangtile tileid="219" wangid="0,0,0,1,0,0,0,0"/>
   <wangtile tileid="220" wangid="0,0,0,1,0,1,0,0"/>
   <wangtile tileid="221" wangid="0,0,0,0,0,1,0,0"/>
   <wangtile tileid="235" wangid="0,1,0,1,0,0,0,0"/>
   <wangtile tileid="236" wangid="0,1,0,1,0,1,0,1"/>
   <wangtile tileid="237" wangid="0,0,0,0,0,1,0,1"/>
   <wangtile tileid="238" wangid="0,1,0,1,0,1,0,0"/>
   <wangtile tileid="239" wangid="0,0,0,1,0,1,0,1"/>
   <wangtile tileid="251" wangid="0,1,0,0,0,0,0,0"/>
   <wangtile tileid="252" wangid="0,1,0,0,0,0,0,1"/>
   <wangtile tileid="253" wangid="0,0,0,0,0,0,0,1"/>
   <wangtile tileid="254" wangid="0,1,0,1,0,0,0,1"/>
   <wangtile tileid="255" wangid="0,1,0,0,0,1,0,1"/>
  </wangset>
 </wangsets>
</tileset>
