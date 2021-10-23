# HistoricalNBBO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**s** | **str** | Symbol. | [optional] 
**skip** | **int** | Number of ticks skipped. | [optional] 
**count** | **int** | Number of ticks returned. If &lt;code&gt;count&lt;/code&gt; &lt; &lt;code&gt;limit&lt;/code&gt;, all data for that date has been returned. | [optional] 
**total** | **int** | Total number of ticks for that date. | [optional] 
**av** | **list[float]** | List of Ask volume data. | [optional] 
**a** | **list[float]** | List of Ask price data. | [optional] 
**ax** | **list[str]** | List of venues/exchanges - Ask price. A list of exchange codes can be found &lt;a target&#x3D;\&quot;_blank\&quot; href&#x3D;\&quot;https://docs.google.com/spreadsheets/d/1Tj53M1svmr-hfEtbk6_NpVR1yAyGLMaH6ByYU6CG0ZY/edit?usp&#x3D;sharing\&quot;,&gt;here&lt;/a&gt; | [optional] 
**bv** | **list[float]** | List of Bid volume data. | [optional] 
**b** | **list[float]** | List of Bid price data. | [optional] 
**bx** | **list[str]** | List of venues/exchanges - Bid price. A list of exchange codes can be found &lt;a target&#x3D;\&quot;_blank\&quot; href&#x3D;\&quot;https://docs.google.com/spreadsheets/d/1Tj53M1svmr-hfEtbk6_NpVR1yAyGLMaH6ByYU6CG0ZY/edit?usp&#x3D;sharing\&quot;,&gt;here&lt;/a&gt; | [optional] 
**t** | **list[int]** | List of timestamp in UNIX ms. | [optional] 
**c** | **list[list[str]]** | List of quote conditions. A comprehensive list of quote conditions code can be found &lt;a target&#x3D;\&quot;_blank\&quot; href&#x3D;\&quot;https://docs.google.com/spreadsheets/d/1iiA6e7Osdtai0oPMOUzgAIKXCsay89dFDmsegz6OpEg/edit?usp&#x3D;sharing\&quot;&gt;here&lt;/a&gt; | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


