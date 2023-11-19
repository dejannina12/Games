// var Student = {
//   name: "Dejan",
//   surname: "Nina",
//   classNumber: "10",
//   school: "sami Frasheri",
//   setSchool: function (newSchool) {
//     console.log(this);
//     this.school = newSchool;
//     if (true) {
//       console.log("this inside if clause", this);
//     }
//   },
// };

// Student.setSchool("Edit durham");

// var Student = function (name, surname, classNumber, school) {
//   this.name = name;
//   this.surname = surname;
//   this.classNumber = classNumber;
//   this.school = school;
//   this.setSchool = function (newSchool) {
//     this.school = newSchool;
//   };
// };

// var student = new Student("Dejan", "Nina", 12, "Edit Durham");
// console.log("student", student.name);
// student.setSchool("Naimi");
// console.log("student", student.school);
// var student2 = new Student("Abi", "Nia", 10, "Sami Frasheri");

var currentCars = [];
var Car = function (model, productionYear, fuel, rent) {
  this.model = model;
  this.productionYear = productionYear;
  this.fuel = fuel;
  this.rent = rent;
};

currentCars.push(new Car("Benz", 2007, "Nafte", 3000));
currentCars.push(new Car("Ford", 2007, "Nafte", 3000));
currentCars.push(new Car("BMV", 2007, "Nafte", 3000));

function rentCar(carModel) {
  for (let i = 0; i < currentCars.length; i++) {
    if (currentCars[i].model === carModel) {
      console.log(i);
      currentCars.splice(i, 1);
      break;
    }
  }
}

function updateCosts(carModel, newCost) {
  for (let i = 0; i < currentCars.length; i++) {
    if (currentCars[i].model === carModel) {
      console.log("Makina u gjet", currentCars[i]);
      currentCars[i].rent = newCost;
      console.log("Makina me kosto te re", currentCars[i]);
    }
  }
}
updateCosts("Benz", 2000);

// rentCar("Ford");
// console.log("Current car after rental", currentCars);
