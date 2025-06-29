# Azure AI Content Safety Container

> ⚠️ **DISCLAIMER:** This software is provided "as is" and the author disclaims all warranties with regard to this software including all implied warranties of merchantability and fitness. In no event shall the author be liable for any special, direct, indirect, or consequential damages or any damages whatsoever resulting from loss of use, data or profits, whether in an action of contract, negligence or other tortious action, arising out of or in connection with the use or performance of this software.
> 
> 🔒 **SECURITY:** This plugin processes text and image content through external API calls to Azure AI Content Safety services. Please ensure you comply with your organization's data privacy policies and Azure's terms of service when using this plugin. The plugin author is not responsible for any data privacy or security issues arising from the use of this software.
>
> 🚨 **DATASET:** The `dataset/` folder contains test data used solely for penetration testing and security validation purposes. This data includes harmful text prompts, offensive language blocklists, and potentially harmful image references. These materials do **NOT** represent the author's views, opinions, beliefs, or values in any way. The author expressly disclaims any association with or endorsement of the content in these test datasets. This data is provided purely for technical testing and should be used responsibly and in compliance with applicable laws and ethical guidelines. Users are solely responsible for how they use this test data.

## Overview

### Azure AI Content Safety

Azure AI Content Safety is an AI service that detects harmful user-generated and AI-generated content in applications and services. Azure AI Content Safety includes text and image APIs that allow you to detect material that is harmful. 

Every harm category the service applies also comes with a severity level rating. The severity level is meant to indicate the severity of the consequences of showing the flagged content.

**1）Harm Categories**

<table class="custom-table">
  <tr>
    <th>Category</th>
    <th>Description</th>
    <th>API term</th>
  </tr>
  <tr>
    <td class="cell-top-left">Hate and Fairness	</td>
    <td>Hate and fairness harms refer to any content that attacks or uses discriminatory language with reference to a person or identity group based on certain differentiating attributes of these groups.

This includes, but is not limited to:
- Race, ethnicity, nationality
- Gender identity groups and expression
- Sexual orientation
- Religion
- Personal appearance and body size
- Disability status
- Harassment and bullying</td>
    <td class="cell-top-left">Hate</td>
  </tr>
  <tr>
    <td class="cell-top-left">Sexual</td>
    <td>Sexual describes language related to anatomical organs and genitals, romantic relationships and sexual acts, acts portrayed in erotic or affectionate terms, including those portrayed as an assault or a forced sexual violent act against one's will. 

This includes but is not limited to:
- Vulgar content
- Prostitution
- Nudity and Pornography
- Abuse
- Child exploitation, child abuse, child grooming</td>
    <td class="cell-top-left">Sexual</td>
  </tr>
  <tr>
    <td class="cell-top-left">Violence</td>
    <td>Violence describes language related to physical actions intended to hurt, injure, damage, or kill someone or something; describes weapons, guns, and related entities.

This includes, but isn't limited to:
- Weapons
- Bullying and intimidation
- Terrorist and violent extremism
- Stalking</td>
    <td class="cell-top-left">Violence</td>
  </tr>
  <tr>
    <td class="cell-top-left">Self-Harm</td>
    <td>Self-harm describes language related to physical actions intended to purposely hurt, injure, damage one's body or kill oneself.

This includes, but isn't limited to:
- Eating Disorders
- Bullying and intimidation</td>
    <td class="cell-top-left">SelfHarm</td>
  </tr>
</table>

**2）Severity Levels**

- **Text**: The current version of the text model supports the full `0-7` severity scale. The classifier detects among all severities along this scale. If the user specifies, it can return severities in the trimmed scale of `0`, `2`, `4`, and `6`; each two adjacent levels are mapped to a single level.
- **Image**: The current version of the image model supports the trimmed version of the full `0-7` severity scale. The classifier only returns severities `0`, `2`, `4`, and `6`.
- **Image with text**: The current version of the multimodal model supports the full `0-7` severity scale. The classifier detects among all severities along this scale. If the user specifies, it can return severities in the trimmed scale of `0`, `2`, `4`, and `6`; each two adjacent levels are mapped to a single level.

### Azure AI Content Safety Container

Containers let you use a subset of the Azure AI Content Safety features in your own environment. With content safety containers, you can build a content safety application architecture optimized for both robust cloud capabilities and edge locality. Containers help you meet specific security and data governance requirements.

**Available Containers:**
- **Analyze text:**	Scans text for sexual content, violence, hate, and self-harm with multiple severity levels.
- **Analyze image:**	Scans images for sexual content, violence, hate, and self-harm with multiple severity levels.

> The content safety container is available in public preview. Containers in preview are still under development and don't meet Microsoft's stability and support requirements.

### Dify Plugin for Azure AI Content Safety Container

This is a Dify plugin that integrates with the [Azure AI Content Safety Container](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview) to analyze both text and image content for harmful material. The plugin can detect various types of harmful content including hate speech, violence, sexual content, and self-harm.

### Features

- **Unified Moderation**: Analyze both text and images in a single tool.
- **Custom Configuration**: Support for custom API endpoints and optional authentication headers.
- **Text Blocklists**: Utilize blocklists for more precise text content filtering.
- **Combined Results**: Get a single, structured result summarizing findings from both text and image analysis.
- **Clear Decisions**: Outputs a clear `ALLOW` or `DENY` check result.
- **Detailed & Formatted Output**: Provides formatted violation details.
- **Raw Data Access**: Includes a `RawResults` output with the original JSON for advanced use cases.

## Configuration

### Prerequisites

**1）Deploy Azure AI Content Safety Container**

Before using this plugin, make sure you have an Azure AI Content Safety Container properly set up and running. See [Install and run content safety containers with Docker](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/how-to/containers/install-run-container) for setup instructions. Please verify that your container is accessible and responding to API requests before configuring this plugin.

**2）Update Dify ENV**

When users send images to the chatbox, `url` that can be used to access the image will be generated in `sys.files` (each image corresponds to one url). The image moderation tool obtains the image by accessing these `url`, converts it to base64, and then sends it to the Image Analyze API for review. Therefore, the correct `FILES_URL` or `CONSOLE_API_URL` must be set in order to generate a corresponding accessible url. Generally, this should be consistent with the main domain name used to access the Dify Portal.

The structure of `sys.files` is as follows:

```json
[
  {
    "dify_model_identity": "__dify__file__",
    "id": null,
    "tenant_id": "7720c6b6-73a5-457f-93a2-66075982fe02",
    "type": "image",
    "transfer_method": "local_file",
    "remote_url": "https://upload.dify.ai/files/xxxxxxxx",
    "related_id": "4763ef42-1bca-44d1-b12b-bee0e841b719",
    "filename": "image_moderation_1.jpg",
    "extension": ".jpg",
    "mime_type": "image/jpeg",
    "size": 39886,
    "url": "https://upload.dify.ai/files/xxxxxxxx"
  }
]
```

### Steps

**1）Get Azure AI Content Safety Container Tools**

Azure AI Content Safety Container can be installed via [Plugin Marketplace](https://marketplace.dify.ai/), [Github](https://github.com/HeyJiqingCode/AzureAIContentSafetyContainer-DifyPlugin.git) or [Local Package File](https://github.com/HeyJiqingCode/AzureAIContentSafetyContainer-DifyPlugin/releases/tag/v0.0.2). Please choose the installation method that best suits your needs. If you are installing via Local Package File, please set `FORCE_VERIFYING_SIGNATURE=false` for the `plugin-daemon` component.

**2）Authentication**

On the Dify navigation page, go to [Tools] > [Azure AI Content Safety Container] > [To Authorize] to fill in the API Endpoint, API Version and optional headers.

![img](./_assets/configuration_steps_1.png)
![img](./_assets/configuration_steps_2.png)

**For example:**

- API Endpoint: `https://xxx.azure-api.net`
- API Version: `2024-05-01`
- Custom Header Key: `Ocp-Apim-Subscription-Key`
- Custom Header Value: `********************************`

**3）Using the tool**

You can use this tool in Chatflow or Workflow. The tool accepts both text and image inputs.

**Parameters:**

- `Text to Analyze`: The text content to analyze.
- `Images to Analyze`: The image files to analyze.
- `Text Blocklist Names`: Comma-separated list of blocklist names for text analysis.
- `Halt on Blocklist Hit`: Whether to stop text analysis if a blocklist item is matched.

**Image Requirements:**
- Maximum size: 7,200 x 7,200 pixels
- Maximum file size: 4 MB
- Minimum size: 50 x 50 pixels

> All parameters are optional. The tool automatically detects when Text or Image inputs are provided (non-empty) and calls the corresponding APIs for content moderation accordingly.

![img](./_assets/use_tool_1.png)
![img](./_assets/use_tool_2.png)

## Output Variables

The tool provides several output variables for use in your workflow:

- `CheckResult`: The final decision (`ALLOW`, `DENY`, or `ERROR`).
- `Details`: A user-friendly, formatted string explaining the violations (only present if `CheckResult` is `DENY`).
- `RawResults`: A JSON object containing the raw, unmodified responses from the Azure APIs. This is useful for custom parsing or logging.

*Example `RawResults` structure:*
```json
{
  "text": {
    "blocklistsMatch": [],
    "categoriesAnalysis": [
      {
        "category": "Hate",
        "severity": 6
      }
    ]
  },
  "image": [
    {
      "categoriesAnalysis": [
        {
          "category": "Sexual",
          "severity": 4
        }
      ]
    }
  ]
}
```

## Examples

**1) Example 1: Text Moderation – Harmful Category**

![img](./_assets/examples_1.png)

**2) Example 2: Text Moderation – Using Block List**

![img](./_assets/examples_2.png)

**3) Example 3: Image Moderation – Harmful Category (Single Image, Multiple Images)**

![img](./_assets/examples_3.png)
![img](./_assets/examples_4.png)

**4) Example 4: Text and Image Moderation with Block List**

![img](./_assets/examples_5.png)

## Test Dataset

The `dataset/` folder contains test data for security validation and penetration testing. **This data does not represent the author's views and is provided solely for technical testing purposes.**

- `harmful_text.csv` - Test prompts for content safety detection
- `test_block_list_cn.csv` - Chinese blocklist for filtering tests  
- `test_block_list_en.csv` - English blocklist for filtering tests
- `harmful_image.csv` - Image references for safety testing

⚠️ **Disclaimer**: Test data is for security validation only. Users are responsible for compliance with applicable laws and ethical guidelines.

## More Details

See [Secure your AI Apps with Azure AI Content Safety Container](https://heyjiqing.notion.site/Secure-your-AI-Apps-with-Azure-AI-Content-Safety-Container-214de7b6e4e88008a072ccb0e6a0f1d6)