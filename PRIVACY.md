### 1. Overview

This privacy policy applies to the Azure AI Content Safety Container plugin (the "Plugin"). The Plugin is developed by [jiqing](https://github.com/HeyJiqingCode) and is designed to provide text content safety detection services for Dify platform users.

### 2. Data Collection

The Plugin processes the following data during operation:

#### 2.1 User Input Data
- **Text Content**: Text content submitted by users for safety detection
- **Configuration Parameters**: Optional parameters such as blocklist names and processing options set by users

#### 2.2 Configuration Data
- **API Endpoint**: Complete Azure AI Content Safety API endpoint URL configured by users
- **Authentication Information**: Optional custom header key-value pairs provided by users for API authentication

### 3. Data Processing

#### 3.1 Local Processing
- The Plugin runs in the local environment and does not send user data to the plugin developer's servers
- All configuration information is stored in the user's Dify instance

#### 3.2 Third-Party Services
- User-submitted text content is sent to the user's configured Azure AI Content Safety API endpoint for analysis
- The Plugin does not control or influence the data processing policies of third-party APIs

### 4. Data Storage

#### 4.1 Local Storage
- Plugin configuration information (API endpoint, authentication information) is securely stored through Dify's credentials mechanism
- Sensitive authentication information is encrypted

#### 4.2 Temporary Data
- Temporary data during text analysis exists only in memory and is not persistently stored
- API response results are used only to generate final safety detection results

### 5. Data Sharing

- The Plugin does not share user data with any third parties
- User data is used only within the scope of the user-configured API endpoint
- Plugin developers cannot access users' specific data content

### 6. Data Security

#### 6.1 Transmission Security
- Communication with Azure AI Content Safety API supports HTTPS encrypted transmission
- Authentication information is passed through secure request headers

#### 6.2 Storage Security
- Sensitive configuration information is protected by Dify platform's encrypted storage mechanism
- Sensitive information is not recorded in log files

### 7. User Rights

Users have the right to:
- Modify or delete plugin configuration information at any time
- Stop using the Plugin
- Understand the specifics of data processing

### 8. Privacy Policy Updates

This privacy policy may be revised based on feature updates or legal requirements. Major updates will be communicated to users through appropriate means.