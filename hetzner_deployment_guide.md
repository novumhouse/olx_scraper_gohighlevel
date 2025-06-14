# Complete Hetzner Cloud Deployment Guide for OLX Job Scraper

## Table of Contents

1. [Introduction and Overview](#introduction)
2. [Why Choose Hetzner Cloud](#why-hetzner)
3. [Prerequisites and Requirements](#prerequisites)
4. [Account Setup and Server Creation](#account-setup)
5. [Server Configuration and Setup](#server-setup)
6. [Application Deployment](#application-deployment)
7. [Automation and Scheduling](#automation)
8. [Monitoring and Maintenance](#monitoring)
9. [Security Configuration](#security)
10. [Cost Analysis and Optimization](#cost-analysis)
11. [Troubleshooting Guide](#troubleshooting)
12. [Advanced Configuration](#advanced-config)

## Introduction and Overview {#introduction}

Deploying your OLX job scraper on Hetzner Cloud provides a robust, cost-effective solution for automated lead generation. This comprehensive guide will walk you through every step of the deployment process, from initial account creation to production-ready automation.

Hetzner Cloud offers exceptional value for hosting automation scripts like your OLX scraper. With servers starting at just €3.29 per month, you can run your scraper 24/7 with excellent reliability and performance. The European data centers are particularly well-suited for scraping Polish websites like OLX.pl, providing low latency and optimal performance.

The deployment process involves several key phases. First, you'll create and configure your Hetzner Cloud account and provision a virtual server. Next, you'll install the necessary software dependencies including Python, Chrome, and the required libraries. Then you'll deploy your OLX scraper application, configure it with your GoHighLevel API credentials, and set up automated scheduling. Finally, you'll implement monitoring, security measures, and maintenance procedures to ensure reliable long-term operation.

This guide assumes you have basic familiarity with Linux command line operations and SSH connections. However, detailed commands and explanations are provided for each step, making it accessible even for users with limited server administration experience.

## Why Choose Hetzner Cloud {#why-hetzner}

Hetzner Cloud stands out as an ideal platform for hosting your OLX scraper for several compelling reasons. The company has built a reputation for providing high-quality infrastructure at competitive prices, making it particularly attractive for small to medium-scale automation projects.

Cost effectiveness represents one of Hetzner's primary advantages. Their CX11 server, priced at €3.29 per month, provides 1 vCPU, 4GB RAM, and 40GB SSD storage with 20TB of included traffic. This configuration is perfectly suited for running web scraping applications that don't require intensive computational resources but benefit from reliable uptime and consistent performance.

The geographic location of Hetzner's data centers provides another significant benefit for your use case. With facilities in Nuremberg, Helsinki, and Ashburn, you can choose a European location that minimizes latency when accessing Polish websites like OLX.pl. This proximity can improve scraping performance and reduce the likelihood of connection timeouts or rate limiting.

Hetzner's infrastructure reliability is backed by enterprise-grade hardware and network connectivity. Their data centers feature redundant power supplies, network connections, and cooling systems, providing 99.9% uptime guarantees. For an automation script that needs to run consistently to capture fresh job listings, this reliability is crucial for maintaining a steady flow of leads.

The platform's scalability options allow you to start small and grow as needed. If your scraping requirements expand or you need additional processing power, you can easily upgrade your server resources without migrating to a different provider. Hetzner offers vertical scaling options up to 96 vCPUs and 384GB RAM for more demanding applications.

Network performance is another area where Hetzner excels. All servers include generous traffic allowances, and the network infrastructure is designed for high throughput and low latency. This ensures your scraper can efficiently download web pages and communicate with external APIs like GoHighLevel without bandwidth constraints.

The user interface and API provided by Hetzner Cloud simplify server management tasks. The web console allows you to monitor resource usage, manage backups, and perform administrative tasks without requiring advanced technical knowledge. For users who prefer programmatic control, the comprehensive API enables automation of server provisioning and management tasks.




## Prerequisites and Requirements {#prerequisites}

Before beginning the deployment process, ensure you have all necessary components and information readily available. Proper preparation will streamline the setup process and minimize potential complications during deployment.

### Technical Requirements

Your local computer should have an SSH client installed for connecting to the remote server. Most modern operating systems include SSH clients by default. Windows users running older versions may need to install PuTTY or enable the Windows Subsystem for Linux to access SSH functionality.

You'll need the updated OLX scraper application files, which should include the main scraper script, GoHighLevel integration module, scheduler, configuration files, and documentation. Ensure you have the latest version that includes the Chrome driver compatibility fixes and improved error handling.

A valid GoHighLevel API key is essential for the integration functionality. This key should have appropriate permissions to create and update contacts in your GoHighLevel account. If you don't have this key readily available, obtain it from your GoHighLevel account settings before proceeding with the deployment.

### Account and Payment Information

A valid email address is required for creating your Hetzner Cloud account. This email will be used for account verification, billing notifications, and important service announcements. Choose an email address that you monitor regularly to ensure you receive critical communications.

Payment method setup requires either a credit card or PayPal account. Hetzner Cloud charges monthly for server usage, and having a valid payment method ensures uninterrupted service. The billing is transparent with no hidden fees, and you can monitor usage and costs through the web console.

Consider your budget requirements for ongoing operation. While the basic CX11 server costs only €3.29 per month, you may want to budget for additional services like automated backups (€1.31 per month) or potential server upgrades if your scraping needs grow over time.

### Security Considerations

SSH key pair generation is highly recommended for secure server access. While password authentication is possible, SSH keys provide superior security and convenience. If you don't already have SSH keys, generate them before creating your server to streamline the initial setup process.

Consider your network security requirements. If you plan to access the server from multiple locations or share access with team members, plan your access control strategy accordingly. Hetzner Cloud supports various authentication methods and firewall configurations to meet different security needs.

### Planning Your Deployment

Determine your scraping schedule and frequency requirements. The default configuration runs the scraper every 24 hours, but you may want to adjust this based on your lead generation needs and OLX.pl's acceptable usage patterns. More frequent scraping may yield more leads but could also increase the risk of rate limiting.

Consider your data retention and backup requirements. The scraper generates log files and result data that accumulate over time. Plan for log rotation and data archival to prevent disk space issues and maintain system performance.

Think about monitoring and alerting needs. While the deployment includes basic monitoring scripts, you may want to implement additional monitoring for critical business processes or integrate with external monitoring services for comprehensive oversight.

## Account Setup and Server Creation {#account-setup}

Creating your Hetzner Cloud account and provisioning your first server involves several straightforward steps. The process is designed to be user-friendly while providing the flexibility needed for various deployment scenarios.

### Account Registration Process

Navigate to the Hetzner Cloud website at https://www.hetzner.com/cloud and locate the registration link. The signup process requires basic information including your name, email address, and contact details. Hetzner may require identity verification for new accounts, particularly for users in certain geographic regions or those requesting higher resource limits.

During registration, you'll need to accept Hetzner's terms of service and privacy policy. These documents outline your rights and responsibilities as a customer, including acceptable use policies that are relevant for web scraping applications. Review these carefully to ensure your intended use case complies with their guidelines.

Email verification is typically required to activate your account. Check your email for a verification message from Hetzner and follow the provided instructions. This step is crucial for account security and ensures you can receive important notifications about your services.

### Payment Method Configuration

After account activation, configure your payment method through the billing section of the web console. Hetzner accepts major credit cards and PayPal for most regions. The payment setup process includes verification steps to prevent fraud and ensure billing accuracy.

Consider enabling automatic payment to avoid service interruptions. Hetzner Cloud services are billed monthly, and failed payments can result in service suspension. Automatic payment ensures continuity of your scraping operations without manual intervention.

Review the billing settings and notification preferences. You can configure alerts for usage thresholds, billing events, and service changes. These notifications help you monitor costs and stay informed about your account status.

### Project Creation and Organization

Hetzner Cloud uses projects to organize resources and manage access control. Create a dedicated project for your OLX scraper deployment to maintain clear separation from other potential projects. Name the project descriptively, such as "OLX-Lead-Generation" or "Job-Scraper-Production."

Project settings allow you to configure default options for new resources, including preferred data center locations and default SSH keys. Setting these preferences streamlines the server creation process and ensures consistency across your infrastructure.

Consider access control requirements if multiple team members will manage the deployment. Hetzner Cloud supports team collaboration features that allow you to grant specific permissions to different users while maintaining security boundaries.

### Server Specification Selection

Choose the appropriate server type based on your performance and budget requirements. The CX11 server type, featuring 1 vCPU, 4GB RAM, and 40GB SSD storage, provides excellent value for most scraping applications. This configuration handles the Chrome browser, Python runtime, and associated processes comfortably while maintaining cost efficiency.

For higher-volume scraping or multiple concurrent scraping processes, consider the CX21 (2 vCPUs, 8GB RAM) or CX31 (2 vCPUs, 16GB RAM) options. These provide additional headroom for processing larger datasets or running multiple scraping instances simultaneously.

Storage requirements are typically modest for scraping applications, as the primary data output consists of JSON files and log entries. The 40GB SSD included with the CX11 server provides ample space for the operating system, application files, and several months of operational data.

### Data Center Location Selection

Select a data center location that optimizes performance for your target websites. For scraping Polish websites like OLX.pl, the Nuremberg data center typically provides the best performance due to its central European location and excellent connectivity to Polish internet infrastructure.

The Helsinki data center offers an alternative European location with similar performance characteristics. This option might be preferable if you plan to expand scraping to other Nordic or Baltic countries in the future.

Consider regulatory and compliance requirements when selecting data center locations. European data centers operate under GDPR and other EU privacy regulations, which may be relevant depending on the nature of the data you're collecting and your business requirements.

### Operating System and Image Selection

Ubuntu 22.04 LTS represents the recommended operating system choice for this deployment. This long-term support release provides stability, security updates, and compatibility with the required software components. The LTS designation ensures continued support and updates for several years, reducing maintenance overhead.

Alternative Linux distributions like Debian or CentOS are also compatible with the deployment scripts, but Ubuntu 22.04 offers the best balance of stability, software availability, and community support for this use case.

Avoid using custom images or snapshots for initial deployment unless you have specific requirements that necessitate them. Starting with a clean Ubuntu installation ensures compatibility with the provided deployment scripts and reduces the likelihood of configuration conflicts.

### Network and Security Configuration

Configure SSH key authentication during server creation to enhance security and streamline access management. Upload your public SSH key through the Hetzner Cloud console, or generate a new key pair if needed. SSH key authentication eliminates the need for password-based login while providing superior security.

Network configuration typically uses default settings for most deployments. Hetzner Cloud automatically assigns public IPv4 and IPv6 addresses to new servers, providing immediate internet connectivity for your scraping application.

Consider firewall requirements during initial setup. While detailed firewall configuration occurs later in the deployment process, understanding your access requirements helps inform initial security planning.

### Server Creation and Initial Access

Complete the server creation process by reviewing all selected options and confirming the configuration. Server provisioning typically completes within 60 seconds, after which you'll receive connection details including the public IP address and initial access credentials.

Record the server's public IP address and any provided access credentials in a secure location. You'll need this information for initial SSH connection and subsequent management tasks.

Test initial connectivity by establishing an SSH connection to your new server. This verification step ensures network connectivity and confirms that your SSH key configuration is working correctly before proceeding with application deployment.


## Server Configuration and Setup {#server-setup}

Once your Hetzner Cloud server is provisioned and accessible, the next phase involves configuring the operating system environment and installing the necessary software components. This process establishes the foundation for your OLX scraper deployment and ensures optimal performance and security.

### Initial System Updates and Security

The first step after connecting to your new server involves updating the operating system packages to their latest versions. This process addresses security vulnerabilities, bug fixes, and compatibility improvements that have been released since the base image was created. Execute the system update process using the package manager's update and upgrade commands.

System updates may require several minutes to complete, depending on the number of available updates and your server's network connectivity. During this process, the system downloads and installs updated packages, which may include kernel updates, security patches, and library improvements that benefit your scraping application.

After completing the initial updates, configure automatic security updates to maintain system security without manual intervention. Ubuntu's unattended-upgrades package provides automated installation of security updates, reducing the administrative overhead while maintaining protection against known vulnerabilities.

Consider configuring a swap file if your server has limited RAM or if you anticipate memory-intensive operations. While the CX11 server's 4GB RAM is typically sufficient for scraping operations, a swap file provides additional virtual memory that can prevent out-of-memory errors during peak usage periods.

### Python Environment Configuration

Python 3.11 or later provides the recommended runtime environment for your OLX scraper application. Ubuntu 22.04 includes Python 3.10 by default, which is compatible with the scraper requirements. Install the python3-pip package manager and python3-venv virtual environment tools to support proper dependency management and isolation.

Virtual environment creation isolates your scraper's Python dependencies from system packages, preventing conflicts and ensuring reproducible deployments. Create a dedicated virtual environment in the application directory and activate it before installing any Python packages.

The pip package manager requires upgrading to the latest version to ensure compatibility with all required packages. Some packages may have specific version requirements or dependencies that are only satisfied by recent pip versions.

Consider installing development tools and compilers if any of your Python dependencies require compilation during installation. The build-essential package provides gcc, make, and other tools that may be needed for packages with native extensions.

### Web Browser and Driver Installation

Chrome or Chromium browser installation is essential for the web scraping functionality. The scraper uses Selenium WebDriver to automate browser interactions, requiring a compatible browser installation. Chromium provides an open-source alternative to Chrome with identical functionality for scraping purposes.

ChromeDriver installation requires careful version matching between the browser and driver versions. Incompatible versions can cause connection failures or unexpected behavior during scraping operations. Download the ChromeDriver version that corresponds to your installed browser version from the official ChromeDriver repository.

Configure the browser for headless operation to optimize resource usage and eliminate the need for a graphical desktop environment. Headless mode provides all necessary functionality for web scraping while reducing memory consumption and improving performance on server environments.

Browser security settings may require adjustment for optimal scraping performance. Disable unnecessary security features that could interfere with automated browsing, such as popup blockers, certificate warnings, and sandbox restrictions that are designed for interactive user sessions.

### System Service Configuration

Systemd service configuration enables automatic startup and management of your scraper application. Create a service unit file that defines how the system should start, stop, and monitor your scraper process. This configuration ensures your scraper continues running after system reboots and provides automatic restart capabilities in case of failures.

Service dependencies should include network connectivity and any required system services. Proper dependency configuration ensures your scraper doesn't attempt to start before essential services are available, preventing startup failures and ensuring reliable operation.

Environment variable configuration through the service file provides a secure method for passing sensitive information like API keys to your application. This approach avoids storing credentials in configuration files while ensuring they're available to the running process.

Logging configuration directs service output to appropriate log files for monitoring and troubleshooting. Configure both standard output and error streams to capture all relevant information for debugging and performance analysis.

### Cron and Scheduling Setup

Cron daemon installation and configuration provides time-based job scheduling capabilities for your scraper. While the application includes its own scheduling logic, cron provides additional flexibility for maintenance tasks, monitoring scripts, and backup operations.

Time zone configuration ensures scheduled tasks execute at the intended times. Set the system timezone to match your business requirements or the timezone of your target market to align scraping schedules with optimal data availability periods.

Cron job configuration requires careful attention to user permissions and environment variables. Jobs running under different user accounts may have different access permissions and environment configurations that could affect script execution.

Consider implementing cron-based monitoring and alerting scripts that check system health, disk usage, and application status. These scripts can provide early warning of potential issues and automate routine maintenance tasks.

### Network and Firewall Configuration

Firewall configuration balances security requirements with operational needs. Configure iptables or ufw to allow necessary inbound connections while blocking unauthorized access attempts. SSH access should be restricted to specific IP addresses or networks when possible.

Outbound network access requires configuration to support web scraping and API communications. Ensure your firewall rules allow connections to target websites, GoHighLevel APIs, and any other external services your scraper requires.

DNS configuration affects the reliability and performance of web requests. Consider using reliable DNS servers like Cloudflare (1.1.1.1) or Google (8.8.8.8) to ensure consistent domain name resolution for target websites.

Network monitoring tools can provide insights into bandwidth usage, connection patterns, and potential network issues. Install and configure tools like netstat, ss, or more advanced monitoring solutions to track network performance and troubleshoot connectivity problems.

## Application Deployment {#application-deployment}

Deploying your OLX scraper application involves transferring the application files to your server, configuring the runtime environment, and establishing the necessary integrations with external services. This process transforms your configured server into a fully functional lead generation system.

### File Transfer and Organization

Application file transfer can be accomplished through several methods, each with specific advantages depending on your local environment and security requirements. Secure Copy Protocol (SCP) provides encrypted file transfer over SSH connections, making it ideal for transferring sensitive application files and configuration data.

Create a dedicated application directory structure that organizes files logically and supports easy maintenance and updates. The recommended structure places application files in /opt/olx-scraper, with subdirectories for logs, configuration, and temporary files. This organization follows Linux filesystem hierarchy standards and simplifies backup and maintenance procedures.

File permissions configuration ensures proper security while allowing necessary access for application execution. Set executable permissions on Python scripts and shell scripts while restricting access to configuration files containing sensitive information like API keys.

Version control integration can simplify future updates and maintenance tasks. Consider initializing a git repository in your application directory to track changes and facilitate rollback procedures if needed.

### Dependency Installation and Configuration

Python package installation should occur within the virtual environment created during server setup. Activate the virtual environment before installing packages to ensure proper isolation and avoid conflicts with system packages.

Requirements file processing automates the installation of all necessary Python dependencies with correct versions. The requirements.txt file specifies exact package versions to ensure reproducible deployments and prevent compatibility issues from version mismatches.

Package compilation may be required for some dependencies, particularly those with native extensions or specific system requirements. Monitor the installation process for compilation errors and install additional development packages if needed.

Dependency verification involves testing that all installed packages function correctly in your server environment. Import each major dependency in a Python shell to confirm successful installation and identify any missing system libraries or configuration issues.

### Configuration File Setup

Environment variable configuration provides a secure and flexible method for managing application settings. Create a .env file containing your GoHighLevel API key, scraping parameters, and other configuration options. This approach separates sensitive information from application code and simplifies configuration management.

Configuration validation ensures all required settings are present and correctly formatted before attempting to run the scraper. Implement validation checks that verify API key format, numeric parameters are within acceptable ranges, and file paths are accessible.

Default configuration values should be appropriate for production use while allowing customization for specific requirements. The provided configuration template includes conservative settings that balance performance with respectful website usage patterns.

Configuration backup procedures protect against accidental loss of settings and simplify disaster recovery. Store configuration files in a secure location separate from the application directory and implement regular backup procedures.

### Database and Storage Configuration

While the OLX scraper primarily uses file-based storage for results and logs, proper storage configuration ensures reliable data persistence and efficient access patterns. Configure log rotation to prevent disk space exhaustion while maintaining sufficient historical data for troubleshooting and analysis.

Result file management involves organizing scraped data in a format that supports easy access and integration with downstream systems. The JSON format provides structured data storage that's compatible with most data processing tools and APIs.

Backup storage configuration protects against data loss and supports disaster recovery procedures. Consider implementing automated backups of result files and configuration data to external storage services or secondary servers.

Storage monitoring helps prevent disk space issues that could interrupt scraper operation. Implement monitoring scripts that track disk usage and alert when storage capacity approaches predefined thresholds.

### Integration Testing and Validation

Initial testing should verify that all application components function correctly in the server environment. Run the scraper in test mode with limited scope to confirm browser automation, web scraping, and data processing capabilities work as expected.

API integration testing validates connectivity and authentication with GoHighLevel services. Test contact creation and update operations using sample data to ensure proper API configuration and permissions.

Error handling validation involves testing the application's response to various failure scenarios, including network timeouts, website changes, and API errors. Verify that error conditions are logged appropriately and don't cause application crashes.

Performance testing establishes baseline metrics for scraping speed, resource usage, and system load. These metrics provide reference points for monitoring production performance and identifying optimization opportunities.

### Production Deployment Preparation

Service registration involves configuring systemd to manage your scraper as a system service. This configuration enables automatic startup, restart on failure, and integration with system monitoring tools.

Monitoring integration establishes the foundation for ongoing operational oversight. Configure log aggregation, performance monitoring, and alerting systems to provide visibility into scraper operation and early warning of potential issues.

Documentation updates should reflect any server-specific configuration changes or customizations made during deployment. Maintain accurate documentation to support future maintenance and troubleshooting activities.

Deployment validation involves comprehensive testing of all functionality in the production environment. Verify that scheduled execution works correctly, results are properly stored and transmitted, and monitoring systems provide appropriate visibility into system operation.

