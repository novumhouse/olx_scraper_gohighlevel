# Complete Hetzner Cloud Deployment Guide for Multi-Client OLX Job Scraper

## Table of Contents

1. [Introduction and Overview](#introduction)
2. [Why Choose Hetzner Cloud](#why-hetzner)
3. [Prerequisites and Requirements](#prerequisites)
4. [Account Setup and Server Creation](#account-setup)
5. [Server Configuration and Setup](#server-setup)
6. [Multi-Client Application Deployment](#application-deployment)
7. [Multi-Client Automation and Scheduling](#automation)
8. [Multi-Client Monitoring and Maintenance](#monitoring)
9. [Security Configuration](#security)
10. [Cost Analysis and Optimization](#cost-analysis)
11. [Troubleshooting Guide](#troubleshooting)
12. [Advanced Multi-Client Configuration](#advanced-config)

## Introduction and Overview {#introduction}

Deploying your multi-client OLX job scraper on Hetzner Cloud provides a robust, cost-effective solution for automated lead generation across multiple clients. This comprehensive guide will walk you through every step of the deployment process, from initial account creation to production-ready multi-client automation.

The multi-client architecture allows you to manage multiple independent clients with separate configurations, API keys, schedules, and data isolation. Each client can have custom search keywords, different scraping frequencies, and isolated result storage, making it perfect for agencies or businesses serving multiple customers.

Hetzner Cloud offers exceptional value for hosting automation scripts like your multi-client OLX scraper. With servers starting at just €3.29 per month, you can run multiple client scrapers 24/7 with excellent reliability and performance. The European data centers are particularly well-suited for scraping Polish websites like OLX.pl, providing low latency and optimal performance.

The multi-client deployment process involves several key phases. First, you'll create and configure your Hetzner Cloud account and provision a virtual server with appropriate resources for multiple clients. Next, you'll install the necessary software dependencies including Python, Chrome, and the required libraries. Then you'll deploy your multi-client OLX scraper application, configure it with multiple client configurations and GoHighLevel API credentials, and set up automated scheduling for each client. Finally, you'll implement monitoring, security measures, and maintenance procedures to ensure reliable long-term operation across all clients.

This guide assumes you have basic familiarity with Linux command line operations and SSH connections. However, detailed commands and explanations are provided for each step, making it accessible even for users with limited server administration experience. The multi-client setup adds additional complexity in configuration management, but provides significant benefits in scalability and client isolation.

## Why Choose Hetzner Cloud {#why-hetzner}

Hetzner Cloud stands out as an ideal platform for hosting your multi-client OLX scraper for several compelling reasons. The company has built a reputation for providing high-quality infrastructure at competitive prices, making it particularly attractive for small to medium-scale automation projects.

Cost effectiveness represents one of Hetzner's primary advantages. Their CX11 server, priced at €3.29 per month, provides 1 vCPU, 4GB RAM, and 40GB SSD storage with 20TB of included traffic. This configuration is perfectly suited for running web scraping applications that don't require intensive computational resources but benefit from reliable uptime and consistent performance.

The geographic location of Hetzner's data centers provides another significant benefit for your use case. With facilities in Nuremberg, Helsinki, and Ashburn, you can choose a European location that minimizes latency when accessing Polish websites like OLX.pl. This proximity can improve scraping performance and reduce the likelihood of connection timeouts or rate limiting.

Hetzner's infrastructure reliability is backed by enterprise-grade hardware and network connectivity. Their data centers feature redundant power supplies, network connections, and cooling systems, providing 99.9% uptime guarantees. For an automation script that needs to run consistently to capture fresh job listings, this reliability is crucial for maintaining a steady flow of leads.

The platform's scalability options allow you to start small and grow as needed. If your scraping requirements expand or you need additional processing power, you can easily upgrade your server resources without migrating to a different provider. Hetzner offers vertical scaling options up to 96 vCPUs and 384GB RAM for more demanding applications.

Network performance is another area where Hetzner excels. All servers include generous traffic allowances, and the network infrastructure is designed for high throughput and low latency. This ensures your scraper can efficiently download web pages and communicate with external APIs like GoHighLevel without bandwidth constraints.

The user interface and API provided by Hetzner Cloud simplify server management tasks. The web console allows you to monitor resource usage, manage backups, and perform administrative tasks without requiring advanced technical knowledge. For users who prefer programmatic control, the comprehensive API enables automation of server provisioning and management tasks.

## Prerequisites and Requirements {#prerequisites}

Before beginning the multi-client deployment process, ensure you have all necessary components and information readily available for each client you plan to manage. Proper preparation will streamline the setup process and minimize potential complications during deployment.

### Technical Requirements

Your local computer should have an SSH client installed for connecting to the remote server. Most modern operating systems include SSH clients by default. Windows users running older versions may need to install PuTTY or enable the Windows Subsystem for Linux to access SSH functionality.

You'll need the updated multi-client OLX scraper application files, which should include the multi-client manager script, multi-client scheduler, core scraper engine, GoHighLevel integration module, client configuration template, and comprehensive documentation. Ensure you have the latest version that includes the Chrome driver compatibility fixes, improved error handling, and multi-client architecture.

**Multiple GoHighLevel API keys** are essential for the multi-client integration functionality. Each client should have their own separate GoHighLevel account and API key with appropriate permissions to create and update contacts. Collect all client API keys before proceeding with the deployment to ensure seamless configuration setup.

### Multi-Client Planning Requirements

**Client Configuration Planning** involves documenting each client's specific requirements including business name, target keywords, scraping frequency preferences, and contact volume expectations. Create a spreadsheet or document listing all clients with their respective configurations before starting the deployment.

**Resource Requirements Assessment** depends on the number of clients you plan to manage. A CX11 server can handle 1-2 clients comfortably, while 3-5 clients may require a CX21 server for optimal performance. Consider the combined resource usage when planning your server specifications.

**Schedule Coordination** requires planning scraping schedules to avoid resource conflicts. Stagger client execution times to prevent multiple Chrome instances from running simultaneously, which could overwhelm server resources and impact performance.

### Account and Payment Information

A valid email address is required for creating your Hetzner Cloud account. This email will be used for account verification, billing notifications, and important service announcements. Choose an email address that you monitor regularly to ensure you receive critical communications.

Payment method setup requires either a credit card or PayPal account. Hetzner Cloud charges monthly for server usage, and having a valid payment method ensures uninterrupted service. The billing is transparent with no hidden fees, and you can monitor usage and costs through the web console.

Consider your budget requirements for ongoing operation. Multi-client deployments may require higher-tier servers (CX21 at €5.83/month or CX31 at €10.52/month) depending on client volume. Budget for additional services like automated backups (€1.31 per month) or potential server upgrades as your client base grows.

### Security Considerations

SSH key pair generation is highly recommended for secure server access. While password authentication is possible, SSH keys provide superior security and convenience. If you don't already have SSH keys, generate them before creating your server to streamline the initial setup process.

**Multi-client security planning** involves protecting sensitive information for multiple clients. Each client's API keys and configuration data must be secured appropriately. Consider access control requirements if multiple team members will manage different clients.

**Client data isolation** ensures that each client's data remains separate and secure. The multi-client architecture provides this isolation through separate configuration files, result files, and log files for each client.

### Planning Your Multi-Client Deployment

**Client scheduling strategy** should optimize resource usage while meeting each client's requirements. Consider time zone differences, target market activity patterns, and server resource availability when planning execution schedules.

**Scalability planning** involves considering future growth in client numbers and adjusting your infrastructure accordingly. Plan for easy addition of new clients and potential server upgrades as your business grows.

**Data retention and backup requirements** multiply with multiple clients. Plan for log rotation, data archival, and backup procedures that handle multiple client datasets efficiently while maintaining data isolation.

**Monitoring and alerting needs** become more complex with multiple clients. Consider implementing client-specific monitoring and alerting to ensure issues with one client don't affect others and to provide appropriate visibility into each client's performance.

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

Hetzner Cloud uses projects to organize resources and manage access control. Create a dedicated project for your multi-client OLX scraper deployment to maintain clear separation from other potential projects. Name the project descriptively, such as "Multi-Client-OLX-Scraper" or "Job-Scraper-Production."

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

Once your Hetzner Cloud server is provisioned and accessible, the next phase involves configuring the operating system environment and installing the necessary software components. This process establishes the foundation for your multi-client OLX scraper deployment and ensures optimal performance and security.

### Initial System Updates and Security

The first step after connecting to your new server involves updating the operating system packages to their latest versions. This process addresses security vulnerabilities, bug fixes, and compatibility improvements that have been released since the base image was created. Execute the system update process using the package manager's update and upgrade commands.

System updates may require several minutes to complete, depending on the number of available updates and your server's network connectivity. During this process, the system downloads and installs updated packages, which may include kernel updates, security patches, and library improvements that benefit your scraping application.

After completing the initial updates, configure automatic security updates to maintain system security without manual intervention. Ubuntu's unattended-upgrades package provides automated installation of security updates, reducing the administrative overhead while maintaining protection against known vulnerabilities.

Consider configuring a swap file if your server has limited RAM or if you anticipate memory-intensive operations. While the CX11 server's 4GB RAM is typically sufficient for scraping operations, a swap file provides additional virtual memory that can prevent out-of-memory errors during peak usage periods.

### Python Environment Configuration

Python 3.11 or later provides the recommended runtime environment for your multi-client OLX scraper application. Ubuntu 22.04 includes Python 3.10 by default, which is compatible with the scraper requirements. Install the python3-pip package manager and python3-venv virtual environment tools to support proper dependency management and isolation.

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

## Multi-Client Application Deployment {#application-deployment}

Deploying your multi-client OLX scraper application involves transferring the application files to your server, configuring the runtime environment, and establishing the necessary integrations with external services. This process transforms your configured server into a fully functional multi-client lead generation system.

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

**Multi-client configuration management** replaces traditional environment variables with a structured JSON configuration file. Create a `clients_config.json` file containing all client configurations with their respective GoHighLevel API keys, scraping parameters, and other client-specific options. This approach provides clear separation between clients while maintaining centralized management.

**Client configuration validation** ensures all required settings are present and correctly formatted for each client before attempting to run the scraper. Implement validation checks that verify API key formats, numeric parameters are within acceptable ranges, file paths are accessible, and client IDs are unique.

**Configuration template structure** should follow the established format for consistent client management:

```json
{
  "clients": {
    "client_id": {
      "name": "Client Display Name",
      "gohighlevel_api_key": "client_api_key_here",
      "search_keywords": ["keyword1", "keyword2", "keyword3"],
      "max_pages": 5,
      "max_listings": 50,
      "schedule_interval_hours": 24,
      "output_file": "results_client_id.json",
      "log_file": "client_id_scraper.log"
    }
  }
}
```

**Configuration security measures** protect sensitive client information through appropriate file permissions and access controls. Set the configuration file to be readable only by the application user and ensure backup procedures maintain the same security level.

**Configuration backup procedures** protect against accidental loss of client settings and simplify disaster recovery. Store configuration files in a secure location separate from the application directory and implement regular backup procedures that maintain client data separation.

### Multi-Client Database and Storage Configuration

**Client-specific storage organization** ensures each client's data remains isolated and easily manageable. Create separate result files, log files, and temporary directories for each client to prevent data mixing and support independent client management.

**Multi-client log rotation** configuration prevents disk space exhaustion while maintaining sufficient historical data for troubleshooting and analysis across all clients. Configure rotation policies that account for varying activity levels between clients.

**Consolidated backup strategies** protect against data loss while maintaining client separation. Implement automated backup procedures that handle multiple client datasets efficiently while preserving data isolation and supporting individual client restore operations.

**Storage monitoring for multiple clients** helps prevent disk space issues that could interrupt scraper operation for any client. Implement monitoring scripts that track disk usage patterns across all clients and alert when storage capacity approaches predefined thresholds.

### Multi-Client Integration Testing and Validation

**Individual client testing** should verify that each client's configuration functions correctly in the server environment. Run each client's scraper in test mode with limited scope to confirm browser automation, web scraping, and data processing capabilities work as expected for their specific configuration.

**Cross-client isolation testing** validates that clients don't interfere with each other during operation. Test concurrent execution scenarios and verify that client-specific data remains separate and secure.

**Multi-client API integration testing** validates connectivity and authentication with GoHighLevel services for each client independently. Test contact creation and update operations using sample data for each client to ensure proper API configuration and permissions across all accounts.

**Scheduler coordination testing** verifies that the multi-client scheduler properly manages execution timing and resource allocation across all configured clients. Test various scheduling scenarios including overlapping execution windows and resource contention situations.

### Production Deployment Preparation

**Multi-client service registration** involves configuring systemd to manage your multi-client scheduler as a system service. This configuration enables automatic startup, restart on failure, and integration with system monitoring tools while managing all clients from a single service.

**Comprehensive monitoring integration** establishes the foundation for ongoing operational oversight across all clients. Configure log aggregation, performance monitoring, and alerting systems that provide visibility into each client's operation while maintaining overall system oversight.

**Client-specific documentation** should reflect any server-specific configuration changes or customizations made during deployment for each client. Maintain accurate documentation that supports future maintenance and troubleshooting activities while preserving client confidentiality.

**Multi-client deployment validation** involves comprehensive testing of all functionality in the production environment for every configured client. Verify that scheduled execution works correctly for each client, results are properly stored and transmitted to the appropriate GoHighLevel accounts, and monitoring systems provide appropriate visibility into each client's operation.

