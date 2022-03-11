/*=== GENERATED BY BIRDWAY VERSION PYA-226DF ===*/
#include <stdio.h>
#include <stdbool.h>
        char EMPTY[] = "";
        const char BIRDWAY_APPLICATION_IDENTIFICATION[] = "greet";
        int birdwayParseOneArgument(char* arg, bool *isShort, char **name, char **value)
        {
            *isShort = false;
            *name = EMPTY;
            *value = arg;
            return 0;
        }
        int birdwayParseAllArguments(int argc, char **argv, void **output)
        {
            bool isShort;
            char *name;
            char *value;
            int pos = 0;
            for (int i=1; i<argc; i++)
            {
                if (birdwayParseOneArgument(argv[i], &pos, &isShort, &name, &value))
                {
                    return 1;
                }
                
                /*printf(isShort ? "yes" : "no");
                printf(" / ");
                printf(name);
                printf(" / ");
                printf(value);
                printf("\n");*/

                
            }
            return 0;
        }
        int birdwayMain(void **globals) 
        {
            return 0;
        }
        int main(int argc, char **argv)
        {
            void *args[1] = {NULL};
            int parsingResult = birdwayParseAllArguments(argc, argv, args);
            if (parsingResult)
            {
                return parsingResult;
            }
            else
            {
                return birdwayMain(args);
            }
        }