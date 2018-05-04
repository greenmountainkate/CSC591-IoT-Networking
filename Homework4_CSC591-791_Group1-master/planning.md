## Homework4_CSC591-791_Group1
CSC 591/791 Group 1 (Omar Chedid, Anirudh Ganji, Athishay Kiran, Katherine Brown) Homework 4

Planning:

- List all modules in project, define inputs and outputs
- Assign ownership and decide on deliverables
- Create namespaces
- Go over Github repo management and version management
- Confirm deliverables match demo requirements


Requirements:

- Timestamp along with decision
- laptop running Bluemix and libSVM

Modules:

- Block 1:  
  - Hardware and Scripts  <b>Status: 90% complete</b>
  
- Block 2:  
  - Raspberry Pi <b>Status: 30% complete - accepting input from IMU via Arduino and saving to file </b>
  - Bluemix Uplink Script
  - (Training Model Script) temp
  
  - Block 2A:
    - Training Model (SVM)
    - Input: a set of files containing raw comma separated IMU values, one sample per row. Format of file name should be <wildcard>_<label:open/close>
    - Example: 
      filename  : sample1_open
      row1      : 0.2,0.3,0.9,12,34,14
    
- Block 3:
  - Classification Model @ Bluemix

- Block 4: 
  - Display decision at local machine
            


Todos:
- Collect data
- Develop Training model
- Test Training model
- Implement in Bluemix
- Develop laptop app to display capture & timestamp
- Complete documentation
