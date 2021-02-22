import random
import datetime
import optparse


def randomize_heart_data(participant_id, timestamp):
    fake_bpm = random.randrange(60, 100)
    query = "INSERT INTO heart_rate VALUES (" + str(participant_id) + ", \'" + \
            timestamp + "\', " + str(fake_bpm) + ");\n"
    return query


def randomize_activity_data(participant_id, timestamp):
    return


def main():
    num_participants = 10
    participant_id = 200
    num_records = 30
    start_time = '2021-2-21 01:00:00'
    insert_participants = False

    print(num_participants, participant_id, num_records, start_time, insert_participants)

    timestamp_format = '%Y-%m-%d %H:%M:%S'
    start_time = datetime.datetime.strptime(start_time, timestamp_format)
    file = open("fake_data_queries.txt", "w")

    for participant in range(num_participants):
        join_date = start_time
        if insert_participants:
            statement = "INSERT INTO participant (participant_id) VALUES (" + str(participant_id) + ");\n"
            file.write(statement)
        for record in range(num_records):
            timestamp = start_time + datetime.timedelta(minutes=record)
            statement = randomize_heart_data(participant_id, timestamp.strftime(timestamp_format))
            file.write(statement)

        participant_id += 1
        file.write("\n")

    file.close()


if __name__ == '__main__':
    main()
