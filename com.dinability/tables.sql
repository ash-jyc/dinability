--
-- Table structure for table `Restaurant`
--
CREATE TABLE `Restaurant` (
    `Restaurant_Name` VARCHAR(50) NOT NULL,
    `Picture_ID` VARCHAR(50) NOT NULL,
    `Description` VARCHAR(50) NOT NULL,
    `Rating_Aspect_1` INT(10),
    `Rating_Aspect_2` INT(10),
    `Rating_Aspect_3` INT(10),
    `Rating_Aspect_4` INT(10),
    `Rating_Aspect_5` INT(10),
    PRIMARY KEY(`Restaurant_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- --------------------------------------------------------

--
-- Table structure for table `Food`
--
CREATE TABLE `Food` (
    `Restaurant_Name` VARCHAR(50) NOT NULL,
    `Food_Name` VARCHAR(50) NOT NULL,
    `Picture_ID` VARCHAR(50) NOT NULL,
    `Description` VARCHAR(50) NOT NULL,
    `Price` INT(10),
    `Rating_Aspect_1` INT(10),
    `Rating_Aspect_2` INT(10),
    `Rating_Aspect_3` INT(10),
    `Rating_Aspect_4` INT(10),
    `Rating_Aspect_5` INT(10),
    PRIMARY KEY(`Restaurant_Name`, `Food_Name`),
    FOREIGN KEY(`Restaurant_Name`) REFERENCES `Restaurant`(`Restaurant_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- --------------------------------------------------------

--
-- Table structure for table `User`
--
CREATE TABLE `User` (
    `User_ID` INT(10) NOT NULL AUTO_INCREMENT,
    `User_Name` VARCHAR(50) NOT NULL,
    `Password` VARCHAR(50) NOT NULL,
    `Rating` INT(10),
    PRIMARY KEY(`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- --------------------------------------------------------

--
-- Table structure for table `Group`
--
CREATE TABLE `Group` (
    `Group_ID` INT(10) NOT NULL AUTO_INCREMENT,
    `Owner_ID` INT(10) NOT NULL,
    `Payment_Method` VARCHAR(50) NOT NULL,
    `Time_Limit` INT(10) NOT NULL,
    `Restaurant_Name` VARCHAR(50) NOT NULL,
    PRIMARY KEY(`Group_ID`),
    FOREIGN KEY(`Owner_ID`) REFERENCES `User`(`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- --------------------------------------------------------

--
-- Table structure for table `Group_Buy_Food`
--
CREATE TABLE `Group_Buy_Food` (
    `Group_ID` INT(10) NOT NULL,
    `Restaurant_Name` VARCHAR(50) NOT NULL,
    `Food_Name` VARCHAR(50) NOT NULL,
    `Time` DATE NOT NULL,
    PRIMARY KEY(`Group_ID`, `Restaurant_Name`, `Food_Name`),
    FOREIGN KEY(`Group_ID`) REFERENCES `Group`(`Group_ID`),
    FOREIGN KEY(`Restaurant_Name`) REFERENCES `Restaurant`(`Restaurant_Name`),
    FOREIGN KEY(`Food_Name`) REFERENCES `Food`(`Food_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- --------------------------------------------------------

--
-- Table structure for table `Group_Buy_Food`
--
CREATE TABLE `Group_Buy_Food` (
    `Group_ID` INT(10) NOT NULL,
    `Restaurant_Name` VARCHAR(50) NOT NULL,
    `Food_Name` VARCHAR(50) NOT NULL,
    `Time` DATE NOT NULL,
    PRIMARY KEY(`Group_ID`, `Restaurant_Name`, `Food_Name`),
    FOREIGN KEY(`Group_ID`) REFERENCES `Group`(`Group_ID`),
    FOREIGN KEY(`Restaurant_Name`, `Food_Name`) REFERENCES `Restaurant`(`Restaurant_Name`, `Food_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- --------------------------------------------------------

--
-- Table structure for table `User_Partipate_in_Group`
--
CREATE TABLE `User_Partipate_in_Group` (
    `User_ID` INT(10) NOT NULL,
    `Group_ID` INT(10) NOT NULL,
    `Time` DATE NOT NULL,
    PRIMARY KEY(`User_ID`, `Group_ID`),
    FOREIGN KEY(`User_ID`) REFERENCES `User`(`User_ID`),
    FOREIGN KEY(`Group_ID`) REFERENCES `Group`(`Group_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- --------------------------------------------------------

--
-- Table structure for table `User_Rate_User`
--
CREATE TABLE `User_Rate_User` (
    `Rater_ID` INT(10) NOT NULL,
    `Ratee_ID` INT(10) NOT NULL,
    `Time` DATE NOT NULL,
    `Rating` INT(10) NOT NULL,
    `Comment` VARCHAR(50),
    PRIMARY KEY(`Rater_ID`, `Ratee_ID`),
    FOREIGN KEY(`Rater_ID`) REFERENCES `User`(`User_ID`),
    FOREIGN KEY(`Ratee_ID`) REFERENCES `User`(`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- --------------------------------------------------------

--
-- Table structure for table `Review_on_Restaurant`
--
CREATE TABLE `Review_on_Restaurant` (
    `User_ID` INT(10) NOT NULL,
    `Time` DATE NOT NULL,
    `Restaurant_Name` VARCHAR(50) NOT NULL,
    `Comment` VARCHAR(50),
    `Rating_Aspect_1` INT(10),
    `Rating_Aspect_2` INT(10),
    `Rating_Aspect_3` INT(10),
    `Rating_Aspect_4` INT(10),
    `Rating_Aspect_5` INT(10),
    PRIMARY KEY(`User_ID`, `Time`),
    FOREIGN KEY(`Rater_ID`) REFERENCES `User`(`User_ID`),
    FOREIGN KEY(`Restaurant_Name`) REFERENCES `Restaurant`(`Restaurant_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- --------------------------------------------------------

--
-- Table structure for table `Review_on_Food`
--
CREATE TABLE `Review_on_Food` (
    `User_ID` INT(10) NOT NULL,
    `Time` DATE NOT NULL,
    `Restaurant_Name` VARCHAR(50) NOT NULL,
    `Food_Name` VARCHAR(50) NOT NULL,
    `Comment` VARCHAR(50),
    `Rating_Aspect_1` INT(10),
    `Rating_Aspect_2` INT(10),
    `Rating_Aspect_3` INT(10),
    `Rating_Aspect_4` INT(10),
    `Rating_Aspect_5` INT(10),
    PRIMARY KEY(`User_ID`, `Time`),
    FOREIGN KEY(`Rater_ID`) REFERENCES `User`(`User_ID`),
    FOREIGN KEY(`Restaurant_Name`, `Food_Name`) REFERENCES `Food`(`Restaurant_Name`, `Food_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- --------------------------------------------------------