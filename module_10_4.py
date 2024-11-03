import threading, time, random, queue

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(random.randint(3, 10))

    def __str__(self):
        return self.name


class Cafe:
    threads = []
    def __init__(self, *tables):
        self.tables = list(tables)
        self.queue = queue.Queue()

    def guest_arrival(self, *guests):
        guests = list(guests)
        for i in range(len(self.tables)):
            self.tables[i].guest = guests[i]
            th = guests[i]
            self.threads.append(th)
            th.start()
            print(f'{guests[i].name} сел(-а) за стол номер {self.tables[i].number}')
        if len(list(guests)) > len(self.tables):
            for i in range(len(self.tables), len(guests)):
                self.queue.put(guests[i])
                print('{0} в очереди'.format(guests[i]))

    def discuss_guests(self):
        while not self.queue.empty() or any([table.guest for table in self.tables]):
            for table in self.tables:
                if not table.guest is None and not table.guest.is_alive():  # is False:
                    print('{0} покушал(-а) и ушёл(ушла).'.format(table.guest))
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                if not self.queue.empty() and table.guest is None:
                    table.guest = self.queue.get()
                    print(f'{table.guest} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    th = table.guest
                    th.start()
                    self.threads.append(th)

# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()

for thread in Cafe.threads:
    thread.join()