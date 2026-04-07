#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <limits.h>

#define USER_DB "users.db"
#define PASSWORD_KEY 'S' // XOR key for encryption/decryption

// XOR encryption/decryption
void encryptDecrypt(char *filename) {
    int fd = open(filename, O_RDWR);
    if (fd < 0) {
        printf("Error opening %s\n", filename);
        return;
    }
    char ch;
    while (read(fd, &ch, 1) == 1) {
        lseek(fd, -1, SEEK_CUR);
        ch ^= PASSWORD_KEY;
        write(fd, &ch, 1);
    }
    close(fd);
    printf("Processed file: %s\n", filename);
}

// Secure delete using unlink()
void secureDelete(char *filename) {
    if (unlink(filename) == 0)
        printf("File %s securely deleted!\n", filename);
    else
        perror("Error deleting file");
}

// Hide file by renaming (prefix with .)
void hideFile(char *filename) {
    char hiddenName[200];
    snprintf(hiddenName, sizeof(hiddenName), ".%s", filename);
    if (rename(filename, hiddenName) == 0)
        printf("File %s hidden as %s\n", filename, hiddenName);
    else
        perror("Error hiding file");
}

// Unhide file by removing leading '.'
void unhideFile(char *filename) {
    if (filename[0] != '.') {
        printf("File %s is not hidden.\n", filename);
        return;
    }
    char unhiddenName[200];
    snprintf(unhiddenName, sizeof(unhiddenName), "%s", filename + 1);
    if (rename(filename, unhiddenName) == 0)
        printf("File %s unhidden as %s\n", filename, unhiddenName);
    else
        perror("Error unhiding file");
}

// Change permissions using chmod()
void changePermissions(char *filename, mode_t mode) {
    if (chmod(filename, mode) == 0)
        printf("Permissions of %s changed successfully.\n", filename);
    else
        perror("Error changing permissions");
}

// Check if user exists in DB
int checkUser(const char *username, const char *password) {
    int fd = open(USER_DB, O_RDONLY);
    if (fd < 0) return 0; // DB does not exist yet

    char buffer[256];
    ssize_t n;
    char fileUser[50], filePass[50];

    while ((n = read(fd, buffer, sizeof(buffer)-1)) > 0) {
        buffer[n] = '\0';
        char *line = strtok(buffer, "\n");
        while (line) {
            sscanf(line, "%s %s", fileUser, filePass);
            if (strcmp(username, fileUser) == 0 && strcmp(password, filePass) == 0) {
                close(fd);
                return 1; // Found
            }
            line = strtok(NULL, "\n");
        }
    }
    close(fd);
    return 0;
}

// Add user to DB
void addUser(const char *username, const char *password) {
    int fd = open(USER_DB, O_CREAT | O_WRONLY | O_APPEND, 0644);
    if (fd < 0) {
        perror("Error creating/opening user DB");
        exit(1);
    }
    char line[256];
    snprintf(line, sizeof(line), "%s %s\n", username, password);
    write(fd, line, strlen(line));
    close(fd);

    char cwd[PATH_MAX];
    getcwd(cwd, sizeof(cwd));
    printf("User database path: %s/%s\n", cwd, USER_DB);
    printf("User %s added successfully.\n", username);
}

// Count users in DB
int countUsers() {
    int fd = open(USER_DB, O_RDONLY);
    if (fd < 0) return 0;
    char buffer[1024];
    ssize_t n = read(fd, buffer, sizeof(buffer));
    close(fd);
    if (n <= 0) return 0;
    int count = 0;
    for (ssize_t i = 0; i < n; i++) {
        if (buffer[i] == '\n') count++;
    }
    return count;
}

// Show vault menu
void showMenu() {
    printf("\n========== Secure File Vault ==========\n");
    printf("1. Encrypt file\n");
    printf("2. Decrypt file\n");
    printf("3. Hide file\n");
    printf("4. Unhide file\n");
    printf("5. Secure delete\n");
    printf("6. Logout\n");
    printf("Enter choice: ");
}

int main() {
    char username[50], password[50];
    int choice;

    // Registration if DB empty
    if (countUsers() == 0) {
        printf("No users found! Please register first.\n");
        printf("Enter new username: ");
        scanf("%s", username);
        printf("Enter new password: ");
        scanf("%s", password);
        addUser(username, password);
    }

    // Login
    printf("\nLogin:\nUsername: ");
    scanf("%s", username);
    printf("Password: ");
    scanf("%s", password);

    if (checkUser(username, password)) {
        printf("Access Granted! Welcome %s\n", username);
    } else {
        printf("User not found. Adding new user.\n");
        addUser(username, password);
        printf("Access Granted! Welcome %s\n", username);
    }

    // Main loop
    while (1) {
        showMenu();
        scanf("%d", &choice);
        char filename[100];
        switch (choice) {
            case 1:
                printf("Enter file to encrypt: ");
                scanf("%s", filename);
                encryptDecrypt(filename);
                break;

            case 2:
                printf("Enter file to decrypt: ");
                scanf("%s", filename);
                encryptDecrypt(filename);
                break;

            case 3:
                printf("Enter file to hide: ");
                scanf("%s", filename);
                hideFile(filename);
                break;

            case 4:
                printf("Enter file to unhide: ");
                scanf("%s", filename);
                unhideFile(filename);
                break;

            case 5:
                printf("Enter file to securely delete: ");
                scanf("%s", filename);
                secureDelete(filename);
                break;

            case 6:
                printf("Logging out...\n");
                exit(0); // ✅ fully exits, no more login loop
                break;

            default:
                printf("Invalid choice! Try again.\n");
        }
    }

    return 0;
}