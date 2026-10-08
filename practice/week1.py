#Exercise 1: Lists
production = [310, 295, 330, 340, 325, 350]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
print(production)
print(len(production))
print(production[0], production[-1])

#Exercise 2: total and average
total = 0
for value in production:
    total = total + value
print("Total:", total)
print("Average:", total / len(production))


#Exercise 3 (finding the biggest value and its position and month)
biggest = max(production)
print(biggest) 
position = production.index(biggest)
print(position)
winner = months[position]
print(winner)

# Exercise 3: functions
def average(numbers):
    total = 0
    for value in numbers:
        total = total + value
    return total / len(numbers)

def biggest_month(months, values):
    biggest = max(values)
    position = values.index(biggest)
    winner = months[position]
    return winner

print(average(production))
print(biggest_month(months, production))

other = [100, 250, 175]
other_months = ["Oct", "Nov", "Dec"]
print(average(other))
print(biggest_month(other_months, other))