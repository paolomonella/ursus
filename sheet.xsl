<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:strip-space elements="*" />

<xsl:template match="/">
  <html>
  <head>
  	<style>
		.LL {color:blue;}
		.AL {color:#B18904;}
		.GL {color:black;}
		.notestyle {
			border:2px dotted black;
			padding:3px;
			margin:3px;
			}
		.disclaimer {
			font-family: Serif;
			border:2px solid black;
			padding:1em;
			margin:1em;
			background-color: #D8D8D8;
			}
		.score {
			font-family: Sans-serif;
			line-height: 7em;
			}
		table {
			line-height: 1em;
			}
	  </style>
  </head>
  <body>
	<h1>Codex Casanatensis 1086</h1>
	<div class="disclaimer">
		<p>An experimental scholarly digital edition by
		<a href="http://www.unipa.it/paolo.monella">Paolo Monella</a>.</p>
		<p><a href="http://www.alim.dfll.univr.it/">ALIM Project</a>,
			2015 (work in progress).</p>
		<p>More information on the Ursus Project in the
			<a href="http://www.unipa.it/paolo.monella/ursus">project home page</a>.
			</p>
		<p>What you see here is the XSLT transformation of the XML/TEI source code.
			To see the source code, just download this page and open
			it with an editor (or use the <code>view source</code>
			option of your browser)</p>
	</div>
  	<div class="score">
		<xsl:apply-templates/>
  	</div>
  </body>
  </html>
</xsl:template>

<!-- Children of w -->

<!-- Notes -->
<!--xsl:template match="//note" mode="note">
	<span style="background-color:red">
	    	<xsl:value-of select="."/>
	</span>
</xsl:template-->

<!--xsl:template match="*" mode="children">
	<xsl:apply-templates mode="lb"/>
	<xsl:apply-templates mode="initial"/>
</xsl:template-->

<!-- Larger initials -->
<xsl:template match="hi[@rend='larger']" mode="initial">
	<b>
	<font size="5">
		<xsl:value-of select="text()"/>
	</font>
			<!-- sgn -->
	</b>
</xsl:template>

<!-- Line breaks -->
<xsl:template match="//lb" mode="lb"><!-- sgn - -->
	<sup>
	<xsl:value-of select="@n"/>
	</sup>
</xsl:template>


<!-- Remove undesired tags from the output -->
<xsl:template match="teiHeader"/>
<xsl:template match="//w"/>
<xsl:template match="//note"/>

<!-- Remove notes -->
<!--xsl:template match="note" mode="noNote">
	<b>
	<xsl:value-of select="."/>
	</b>
</xsl:template-->

<xsl:template match="note" mode="note">
	<xsl:choose>
		<xsl:when test="@type='script'">
			<span class="notestyle" style="background-color:#F2F5A9">
			<em><xsl:text>Palaeographic note: </xsl:text></em>
			<xsl:value-of select="text()"/>
			</span>
		</xsl:when>
		<xsl:when test="@type='source'">
			<span class="notestyle" style="background-color:#A9E2F3">
			<em><xsl:text>Note on the literary sources: </xsl:text></em>
			<xsl:value-of select="."/>
			</span>
		</xsl:when>
		<xsl:when test="@type='content'">
			<span class="notestyle" style="background-color:#A9F5A9">
			<em><xsl:text>Note on the textual content: </xsl:text></em>
			<xsl:value-of select="."/>
			</span>
		</xsl:when>
		<xsl:when test="@type='tech'">
			<span class="notestyle" style="background-color:#E6E6E6">
			<em><xsl:text>Technological note: </xsl:text></em>
			<xsl:value-of select="."/>
			</span>
		</xsl:when>
	</xsl:choose>
</xsl:template>


<!-- Punctuation -->
<xsl:template match="//pc">
	<table style="display:inline">
	  <tr class="LL"><td>
		<xsl:choose>
			<xsl:when test="@ana='quote'">
				<xsl:text>"</xsl:text>
			</xsl:when>
			<xsl:when test="@ana='question'">
				<xsl:text>?</xsl:text>
			</xsl:when>
			<xsl:when test="@ana='0'">
				<xsl:text>&#160;</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="@ana"/>
			</xsl:otherwise>
		</xsl:choose>
	  </td></tr>
	  <tr class="AL"><td>&#160;</td></tr>
	  <tr class="GL"><td><xsl:value-of select="text()"/>
	  </td></tr>
	</table>
</xsl:template>

<!-- Space -->
<xsl:template match="pc[@ana='space']">
<!--xsl:template match="ref/text() | head/text()"-->
<!--This matches '_' characters representing space-->
		<!--span style="background-color:grey">_</spanr-->
	<table style="display:inline">
	  <tr class="LL"><td>&#160;</td></tr>
	  <tr class="AL"><td>&#160;</td></tr>
	  <tr class="GL"><td bgcolor="grey">&#160;</td></tr>
	</table>
</xsl:template>



<!-- Alphabetic layer of all words -->

<xsl:template match="choice/abbr"  mode="alphabetic"/>
<xsl:template match="text()"  mode="alphabetic">
	<xsl:value-of select="normalize-space(.)" />
</xsl:template>

<!-- Graphematic layer of abbreviations -->

<xsl:template match="choice/expan" mode="graphematic-brev"/>
<xsl:template match="text()"  mode="graphematic-brev">
	<xsl:value-of select="normalize-space(.)" />
</xsl:template>

<xsl:template match="choice/expan" mode="graphematic-after"/>
<xsl:template match="text()"  mode="graphematic-after">
	<xsl:value-of select="normalize-space(.)" />
</xsl:template>

<xsl:template match="choice/expan" mode="graphematic-super"/>
<xsl:template match="choice/abbr" mode="graphematic-super">
	<table style="display:inline">
	  <tr>
	    <td>
	    <xsl:value-of select="am"/>
	    </td>
	  </tr>
	  <tr>
	    <td>
	    <xsl:value-of select="text()"/>
	    </td>
	  </tr>
	</table>
</xsl:template>
<xsl:template match="text()"  mode="graphematic-super">
	<xsl:value-of select="normalize-space(.)" />
</xsl:template>


<!-- Words without abbreviations -->
<xsl:template match="//w[not(choice)]">
		<table style="display:inline">
		  <tr class="LL">
		    <td>
		      <xsl:value-of select="@ana"/>
		    </td>
		  </tr>
		  <tr class="AL">
		    <td>
			<xsl:choose>
			  <xsl:when test="not(note)">
			    <xsl:apply-templates mode="lb"/>
			  </xsl:when>
			  <xsl:when test="note">
			    	<xsl:value-of select="text()"/>
			  </xsl:when>
			</xsl:choose>
		    </td>
		  </tr>
		  <tr class="GL">
		    <td>
			<!-- sgn -->
			<!--xsl:apply-templates mode="children"/-->
			<xsl:if test="hi[@rend='larger']">
			  <font color="grey"><b>↑</b></font>
			</xsl:if>
			<!--xsl:apply-templates mode="initial"/-->
			<xsl:choose>
			  <xsl:when test="not(note)">
			    <xsl:apply-templates mode="lb"/>
			  </xsl:when>
			  <xsl:when test="note">
			    	<xsl:value-of select="text()"/>
			  </xsl:when>
			</xsl:choose>
			<!--xsl:apply-templates mode="lb"/-->
		    </td>
		  </tr>
		</table>
		<xsl:if test="note">
			<xsl:apply-templates mode="note"/>
		</xsl:if>
	<!--xsl:if test="hi">
		<span style="background-color:green">
		    	<xsl:value-of select="hi"/>
		</span>
	</xsl:if-->
</xsl:template>



<!-- Words with abbreviations -->
<xsl:template match="//w[choice]">
	<xsl:choose>
		<xsl:when test="note"/>
		<xsl:when test="choice/abbr[@type='brevigraph']">
			<table style="display:inline">
			  <tr class="LL">
			    <td>
			      <xsl:value-of select="@ana"/>
			    </td>
			  </tr>
			  <tr class="AL">
			    <td>
			      <xsl:apply-templates mode="alphabetic"/>
			    </td>
			  </tr>
			  <tr class="GL">
			    <td>
			      <xsl:apply-templates mode="graphematic-brev"/>
			    </td>
			  </tr>
			</table>
		</xsl:when>
		<xsl:when test="choice/abbr[@type='superscription']">
			<table style="display:inline">
			  <tr class="LL">
			    <td>
			      <xsl:value-of select="@ana"/>
			    </td>
			  </tr>
			  <tr class="AL">
			    <td>
			      <xsl:apply-templates mode="alphabetic"/>
			    </td>
			  </tr>
			  <tr class="GL">
			    <td>
			      <xsl:apply-templates mode="graphematic-super"/>
			    </td>
			  </tr>
			</table>
		</xsl:when>
		<xsl:when test="choice/abbr[@type='after']">
			<table style="display:inline">
			  <tr class="LL">
			    <td>
			      <xsl:value-of select="@ana"/>
			    </td>
			  </tr>
			  <tr class="AL">
			    <td>
			      <xsl:apply-templates mode="alphabetic"/>
			    </td>
			  </tr>
			  <tr class="GL">
			    <td>
			      <xsl:apply-templates mode="graphematic-after"/>
			    </td>
			  </tr>
			</table>
		</xsl:when>
	        <xsl:otherwise>
			<xsl:value-of select="."/>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:if test="note">
		<xsl:apply-templates mode="note"/>
	</xsl:if>
</xsl:template>





</xsl:stylesheet> 
