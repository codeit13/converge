<template>
  <div
    class="w-full flex flex-col items-center justify-center overflow-hidden relative"
    :style="{
      fontFamily: `'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif`,
    }"
  >
    <Card
      class="w-fit flex flex-col flex-1 overflow-hidden shadow-md border border-zinc-200 dark:border-zinc-700 m-0 sm:m-4 md:m-6 rounded-xl bg-transparent"
    >
      <CardHeader
        class="border-b border-zinc-200 dark:border-zinc-700 py-4 px-4 sm:py-5 sm:px-6 flex flex-col md:flex-row md:items-center md:justify-between gap-2"
      >
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-2">
            <div class="p-2 rounded-lg">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="text-zinc-700 dark:text-zinc-300"
              >
                <path
                  d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"
                />
                <path d="M18 14h-8" />
                <path d="M15 18h-5" />
                <path d="M10 6h8v4h-8V6Z" />
              </svg>
            </div>
            <div>
              <CardTitle
                class="font-display text-xl md:text-2xl dark:text-zinc-100"
                >Knowledge Base</CardTitle
              >
              <CardDescription
                class="text-sm mt-1 text-zinc-600 dark:text-zinc-400"
              >
                Store and search through your custom data sources
              </CardDescription>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent
        class="flex flex-col gap-5 sm:gap-7 px-4 py-4 sm:px-6 sm:py-6 flex-1 overflow-y-auto custom-scrollbar"
      >
        <!-- Add Document Section -->
        <Card
          class="bg-transparent border border-zinc-200 dark:border-zinc-700 shadow-sm"
        >
          <CardHeader class="py-3 px-4">
            <CardTitle class="text-base dark:text-zinc-100"
              >Add to Knowledge Base</CardTitle
            >
            <CardDescription class="text-xs text-zinc-600 dark:text-zinc-400">
              Choose a source type and add content to your knowledge base
            </CardDescription>
          </CardHeader>
          <CardContent class="py-3 px-4">
            <form
              @submit.prevent="handleAddDocument"
              class="flex flex-col gap-4"
            >
              <!-- Source Type Pills -->
              <div class="flex flex-wrap gap-2">
                <button
                  type="button"
                  @click="sourceType = 'text'"
                  class="px-3 py-1.5 text-sm rounded-full transition-all duration-200 flex gap-2 items-center"
                  :class="
                    sourceType === 'text'
                      ? 'bg-zinc-200 dark:bg-zinc-700 text-zinc-800 dark:text-zinc-200 font-medium'
                      : 'bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 text-zinc-700 dark:text-zinc-300'
                  "
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <polyline points="4 7 4 4 20 4 20 7" />
                    <line x1="9" x2="15" y1="20" y2="20" />
                    <line x1="12" x2="12" y1="4" y2="20" />
                  </svg>
                  Text
                </button>
                <button
                  type="button"
                  @click="sourceType = 'url'"
                  class="px-3 py-1.5 text-sm rounded-full transition-all duration-200 flex gap-2 items-center"
                  :class="
                    sourceType === 'url'
                      ? 'bg-zinc-200 dark:bg-zinc-700 text-zinc-800 dark:text-zinc-200 font-medium'
                      : 'bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 text-zinc-700 dark:text-zinc-300'
                  "
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"
                    />
                    <path
                      d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"
                    />
                  </svg>
                  URL
                </button>
                <button
                  type="button"
                  @click="sourceType = 'file'"
                  class="px-3 py-1.5 text-sm rounded-full transition-all duration-200 flex gap-2 items-center"
                  :class="
                    sourceType === 'file'
                      ? 'bg-zinc-200 dark:bg-zinc-700 text-zinc-800 dark:text-zinc-200 font-medium'
                      : 'bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 text-zinc-700 dark:text-zinc-300'
                  "
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"
                    />
                    <polyline points="17 21 17 13 7 13 7 21" />
                    <polyline points="7 3 7 8 15 8" />
                  </svg>
                  File
                </button>
              </div>

              <!-- Dynamic Input Based on Source Type -->
              <div class="w-full transition-all duration-200 ease-in-out">
                <div v-if="sourceType === 'text'" class="space-y-2">
                  <Label
                    for="content"
                    class="text-sm text-zinc-700 dark:text-zinc-300"
                    >Text Content</Label
                  >
                  <Textarea
                    v-model="content"
                    id="content"
                    placeholder="Enter text to add to your knowledge base..."
                    class="resize-none focus:ring-1 focus:ring-zinc-400 dark:focus:ring-zinc-600 transition-all duration-200 bg-white dark:bg-zinc-800 border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-200 placeholder-zinc-400 dark:placeholder-zinc-500 w-full"
                    rows="4"
                  />
                  <p class="text-xs text-zinc-500 dark:text-zinc-400">
                    Add paragraphs, snippets, or any text content
                  </p>
                </div>

                <div v-if="sourceType === 'url'" class="space-y-2">
                  <Label
                    for="content"
                    class="text-sm text-zinc-700 dark:text-zinc-300"
                    >URL</Label
                  >
                  <Input
                    v-model="content"
                    id="content"
                    placeholder="https://example.com/article"
                    class="focus:ring-1 focus:ring-zinc-400 dark:focus:ring-zinc-600 transition-all duration-200 bg-white dark:bg-zinc-800 border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-200 placeholder-zinc-400 dark:placeholder-zinc-500 w-full"
                  />
                  <p class="text-xs text-zinc-500 dark:text-zinc-400">
                    The system will extract and process content from this URL
                  </p>
                </div>

                <div v-if="sourceType === 'file'" class="space-y-2">
                  <Label
                    for="fileInput"
                    class="text-sm text-zinc-700 dark:text-zinc-300"
                    >Upload File</Label
                  >
                  <div
                    class="border-2 border-dashed border-zinc-300 dark:border-zinc-700 rounded-lg p-4 sm:p-6 text-center hover:bg-zinc-50 dark:hover:bg-zinc-800/80 cursor-pointer transition-colors"
                  >
                    <input
                      type="file"
                      ref="fileInput"
                      id="fileInput"
                      accept="*"
                      class="hidden"
                      @change="handleFileChange"
                    />
                    <div
                      class="flex flex-col items-center justify-center gap-2"
                      @click="triggerFileUpload"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="text-zinc-400 dark:text-zinc-500"
                      >
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" x2="12" y1="3" y2="15" />
                      </svg>
                      <div v-if="selectedFile">
                        <p
                          class="text-sm font-medium text-zinc-700 dark:text-zinc-300"
                        >
                          {{ selectedFile.name }}
                        </p>
                        <p class="text-xs text-zinc-500 dark:text-zinc-400">
                          {{ formatFileSize(selectedFile.size) }}
                        </p>
                      </div>
                      <div v-else>
                        <p
                          class="text-sm font-medium text-zinc-700 dark:text-zinc-300"
                        >
                          Drag & drop or click to upload
                        </p>
                        <p class="text-xs text-zinc-500 dark:text-zinc-400">
                          Supports PDF, TXT, DOCX, and more
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="flex justify-end mt-2">
                <Button
                  type="submit"
                  variant="default"
                  class="w-full sm:w-auto group transition-all duration-200 hover:shadow-md bg-zinc-800 hover:bg-zinc-700 text-white dark:bg-zinc-700 dark:hover:bg-zinc-600 dark:text-zinc-100"
                  :disabled="!isFormValid"
                  :class="{ 'opacity-50 cursor-not-allowed': !isFormValid }"
                >
                  <span class="flex items-center gap-2">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="group-hover:translate-x-0.5 transition-transform duration-200"
                    >
                      <path d="M5 12h14" />
                      <path d="m12 5 7 7-7 7" />
                    </svg>
                    Add to Knowledge Base
                  </span>
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        <!-- Search Form -->
        <div class="space-y-3">
          <Label
            for="searchQuery"
            class="text-sm font-medium text-zinc-700 dark:text-zinc-300"
            >Search Knowledge Base</Label
          >
          <form
            @submit.prevent="handleSearch"
            class="flex flex-col sm:flex-row gap-2 relative"
          >
            <div class="relative flex-1">
              <Input
                v-model="searchQuery"
                id="searchQuery"
                placeholder="Search for documents, facts, or answers..."
                class="pl-10 focus:ring-1 focus:ring-zinc-400 dark:focus:ring-zinc-600 transition-all duration-200 bg-white dark:bg-zinc-800 border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-200 placeholder-zinc-400 dark:placeholder-zinc-500 w-full"
              />
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-zinc-500"
              >
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.3-4.3" />
              </svg>
            </div>
            <Button
              type="submit"
              variant="outline"
              class="bg-white dark:bg-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-700 border-zinc-300 dark:border-zinc-700 hover:border-zinc-400 dark:hover:border-zinc-600 transition-all duration-200 text-zinc-700 dark:text-zinc-300"
            >
              Search
            </Button>
          </form>
        </div>

        <!-- Results Section -->
        <div class="flex flex-col gap-4">
          <div v-if="searchResults.length">
            <div class="font-semibold text-base mb-3 flex items-center gap-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="text-zinc-700 dark:text-zinc-300"
              >
                <path d="m22 2-7 20-4-9-9-4Z" />
                <path d="M22 2 11 13" />
              </svg>
              <span class="text-zinc-800 dark:text-zinc-100"
                >Search Results</span
              >
              <span class="text-xs font-normal text-zinc-500 dark:text-zinc-400"
                >{{ searchResults.length }} document(s) found</span
              >
            </div>
            <div class="space-y-3">
              <div
                v-for="doc in searchResults"
                :key="doc.doc_id"
                class="rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 hover:shadow-md transition-all duration-200 p-4 flex flex-col gap-3"
              >
                <div class="flex items-start justify-between gap-3">
                  <div class="flex-1 min-w-0">
                    <div
                      class="font-medium text-base truncate text-zinc-800 dark:text-zinc-200"
                    >
                      {{ doc.doc_id }}
                    </div>
                    <p
                      class="text-sm text-zinc-600 dark:text-zinc-400 line-clamp-2"
                    >
                      {{ doc.content_preview }}
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    class="text-zinc-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 flex-shrink-0 -mt-1 -mr-2"
                    title="Delete document"
                    @click="confirmDelete(doc.doc_id)"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="18"
                      height="18"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path d="M3 6h18" />
                      <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                      <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                      <line x1="10" x2="10" y1="11" y2="17" />
                      <line x1="14" x2="14" y1="11" y2="17" />
                    </svg>
                  </Button>
                </div>
                <div
                  class="text-xs px-2 py-1 rounded bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 font-mono break-all max-w-full overflow-x-auto scrollbar-thin"
                >
                  {{
                    doc.metadata && typeof doc.metadata === "object"
                      ? JSON.stringify(doc.metadata, null, 2)
                      : doc.metadata
                  }}
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <div class="font-semibold text-base mb-3 flex items-center gap-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="text-zinc-700 dark:text-zinc-300"
              >
                <path
                  d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"
                />
                <path d="M14 2v6h6" />
              </svg>
              <span class="text-zinc-800 dark:text-zinc-100">Documents</span>
              <span
                class="text-xs font-normal text-zinc-500 dark:text-zinc-400"
                v-if="documents.length"
                >{{ documents.length }} document(s) in database</span
              >
            </div>
            <div
              v-if="documents.length === 0"
              class="text-zinc-400 italic bg-zinc-50 dark:bg-zinc-800/50 border border-dashed border-zinc-200 dark:border-zinc-700 rounded-xl p-8 text-center"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="40"
                height="40"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="mx-auto mb-3 text-zinc-300 dark:text-zinc-600"
              >
                <path
                  d="M2 9V5c0-1.1.9-2 2-2h3.93a2 2 0 0 1 1.66.9l.82 1.2a2 2 0 0 0 1.66.9H20a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-1"
                />
                <path d="M2 13h10" />
                <path d="m5 10-3 3 3 3" />
              </svg>
              <p class="mb-1 text-zinc-500 dark:text-zinc-400">
                No documents in your knowledge base yet
              </p>
              <p class="text-sm text-zinc-400 dark:text-zinc-500">
                Add text, URLs, or files using the form above
              </p>
            </div>
            <div v-else>
              <!-- Single Accordion for all documents -->
              <Accordion :collapsible="true" class="border-none space-y-4">
                <!-- Document Cards as AccordionItems -->
                <AccordionItem
                  v-for="doc in documents"
                  :key="doc.doc_id"
                  :value="doc.doc_id"
                  class="border-none rounded-xl border border-zinc-200 dark:border-zinc-700 bg-primary/10 dark:bg-secondary/10 hover:shadow-md transition-all duration-200 overflow-hidden group"
                >
                  <!-- Card Header and Preview Content -->
                  <div class="p-4">
                    <!-- Document Header with Icon and Delete Button -->
                    <div class="flex items-start justify-between gap-3">
                      <div class="flex items-start gap-3">
                        <div
                          class="p-2 rounded-md bg-primary/5 dark:bg-primary/10 flex-shrink-0"
                        >
                          <!-- Document icon based on source type if available -->
                          <svg
                            v-if="getDocSourceType(doc) === 'url'"
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            class="text-zinc-600 dark:text-zinc-300"
                          >
                            <path
                              d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"
                            ></path>
                            <path
                              d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"
                            ></path>
                          </svg>
                          <svg
                            v-else-if="getDocSourceType(doc) === 'file'"
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            class="text-zinc-600 dark:text-zinc-300"
                          >
                            <path
                              d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"
                            ></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                          </svg>
                          <svg
                            v-else
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            class="text-zinc-600 dark:text-zinc-300"
                          >
                            <path
                              d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                            ></path>
                            <path d="M14 2v6h6"></path>
                            <path d="M16 13H8"></path>
                            <path d="M16 17H8"></path>
                            <path d="M10 9H8"></path>
                          </svg>
                        </div>
                        <div class="flex-1 min-w-0">
                          <h4
                            class="text-base font-medium text-zinc-800 dark:text-zinc-200 truncate"
                          >
                            {{ getDocTitle(doc) }}
                          </h4>
                          <p
                            class="text-xs text-zinc-500 dark:text-zinc-400 truncate"
                          >
                            ID: {{ shortenDocId(doc.doc_id) }}
                          </p>
                        </div>
                      </div>

                      <!-- Delete Button (only visible on hover) -->
                      <button
                        @click.stop="confirmDelete(doc.doc_id)"
                        class="text-zinc-400 hover:text-red-500 dark:text-zinc-500 dark:hover:text-red-400 transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
                        title="Delete document"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="16"
                          height="16"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        >
                          <path d="M3 6h18"></path>
                          <path
                            d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"
                          ></path>
                          <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                        </svg>
                      </button>
                    </div>

                    <!-- Document Content Preview -->
                    <p
                      class="text-sm text-zinc-600 dark:text-zinc-400 line-clamp-2 mt-2"
                    >
                      {{ doc.content_preview }}
                    </p>

                    <!-- Basic Metadata Preview -->
                    <div class="mt-2 space-y-1">
                      <!-- Source URL with icon if available -->
                      <div
                        v-if="getDocMetadata(doc, 'source')"
                        class="flex items-center gap-1.5 text-xs font-bold text-zinc-500 dark:text-zinc-400"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="12"
                          height="12"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          class="text-secondary dark:text-secondary"
                        >
                          <path
                            d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"
                          ></path>
                          <path
                            d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"
                          ></path>
                        </svg>
                        <a
                          :href="getDocMetadata(doc, 'source')"
                          target="_blank"
                          class="text-secondary dark:text-secondary truncate"
                          title="Open source URL"
                        >
                          {{ formatUrl(getDocMetadata(doc, "source")) }}
                        </a>
                      </div>
                    </div>
                  </div>

                  <!-- Accordion Trigger for Details -->
                  <AccordionTrigger
                    class="px-4 py-2 text-xs text-black hover:text-black/80 dark:text-white dark:hover:text-white/80 transition-colors border-t border-zinc-100 dark:border-zinc-700/50 hover:bg-zinc-50 dark:hover:bg-zinc-800/80"
                  >
                    <span>View Details</span>
                  </AccordionTrigger>

                  <!-- Accordion Content with Full Details -->
                  <AccordionContent
                    class="px-4 pb-4 pt-2 bg-zinc-50 dark:bg-zinc-800/80 border-t border-zinc-100 dark:border-zinc-700/50"
                  >
                    <div class="space-y-3">
                      <!-- Full Content Preview -->
                      <div>
                        <div
                          class="text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1"
                        >
                          Content:
                        </div>
                        <p class="text-sm text-zinc-600 dark:text-zinc-400">
                          {{ doc.content_preview }}
                        </p>
                      </div>

                      <!-- Language if available -->
                      <div
                        v-if="getDocMetadata(doc, 'language')"
                        class="flex items-center gap-1.5 text-xs text-zinc-500 dark:text-zinc-400"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="12"
                          height="12"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          class="text-primary dark:text-primary-foreground"
                        >
                          <path d="m5 8 6 6"></path>
                          <path d="m4 14 10-10 6 6-10 10-6-6z"></path>
                        </svg>
                        <span class="capitalize">{{
                          getDocMetadata(doc, "language")
                        }}</span>
                      </div>

                      <!-- Description if available -->
                      <div v-if="getDocMetadata(doc, 'description')">
                        <div
                          class="text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1"
                        >
                          Description:
                        </div>
                        <div class="text-xs text-zinc-600 dark:text-zinc-400">
                          {{ getDocMetadata(doc, "description") }}
                        </div>
                      </div>

                      <!-- Full metadata -->
                      <div v-if="doc.metadata" class="pt-2">
                        <div
                          class="text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1"
                        >
                          Full Metadata:
                        </div>
                        <pre
                          class="text-xs bg-secondary/5 dark:bg-secondary/10 p-2 rounded text-zinc-600 dark:text-zinc-300 overflow-x-auto scrollbar-thin"
                          >{{ formatMetadata(doc.metadata) }}</pre
                        >
                      </div>
                    </div>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Delete Confirmation Dialog (appears when deleteConfirmDocId is set) -->
    <div
      v-if="deleteConfirmDocId"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50"
    >
      <div
        class="bg-white dark:bg-zinc-800 rounded-lg shadow-lg max-w-md w-full p-6 mx-4"
      >
        <h3 class="text-lg font-semibold mb-2 text-zinc-800 dark:text-zinc-100">
          Confirm Delete
        </h3>
        <p class="text-zinc-600 dark:text-zinc-400 mb-4">
          Are you sure you want to delete this document? This action cannot be
          undone.
        </p>
        <div class="flex justify-end gap-3">
          <Button
            variant="outline"
            class="border-zinc-300 dark:border-zinc-600 text-zinc-700 dark:text-zinc-300"
            @click="deleteConfirmDocId = null"
            >Cancel</Button
          >
          <Button
            variant="destructive"
            class="bg-red-500 hover:bg-red-600 text-white"
            @click="proceedWithDelete"
          >
            <span class="flex items-center gap-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M3 6h18" />
                <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
              </svg>
              Delete Document
            </span>
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 1. Third-party imports
import { mapActions, mapState } from "vuex";
// 2. Component imports
import Input from "@/components/ui/input/Input.vue";
import Button from "@/components/ui/button/Button.vue";
import Select from "@/components/ui/select/Select.vue";
import Card from "@/components/ui/card/Card.vue";
import CardHeader from "@/components/ui/card/CardHeader.vue";
import CardTitle from "@/components/ui/card/CardTitle.vue";
import CardDescription from "@/components/ui/card/CardDescription.vue";
import CardContent from "@/components/ui/card/CardContent.vue";
import Label from "@/components/ui/label/Label.vue";
import Textarea from "@/components/ui/textarea/Textarea.vue";
import Accordion from "@/components/ui/accordion/Accordion.vue";
import AccordionItem from "@/components/ui/accordion/AccordionItem.vue";
import AccordionTrigger from "@/components/ui/accordion/AccordionTrigger.vue";
import AccordionContent from "@/components/ui/accordion/AccordionContent.vue";

export default {
  name: "KnowledgeBaseView",
  components: {
    Input,
    Button,
    Select,
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent,
    Label,
    Textarea,
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
  },
  data() {
    return {
      sourceType: "text",
      content: "",
      searchQuery: "",
      searchResults: [],
      selectedFile: null,
      deleteConfirmDocId: null,
      expandedDocs: {}, // Tracks which documents are expanded to show full details
    };
  },
  computed: {
    ...mapState(["documents"]),
    isFormValid() {
      if (this.sourceType === "text") {
        return this.content.trim().length > 0;
      } else if (this.sourceType === "url") {
        return this.content.trim().startsWith("http");
      } else if (this.sourceType === "file") {
        return this.selectedFile !== null;
      }
      return false;
    },
  },
  async mounted() {
    await this.loadDocuments();
  },
  methods: {
    ...mapActions([
      "ragAddDocument",
      "ragGetDocuments",
      "ragDeleteDocument",
      "ragSearchDocuments",
    ]),
    async handleAddDocument() {
      if (!this.isFormValid) return;

      let payload = { sourceType: this.sourceType };
      if (this.sourceType === "file") {
        payload.file = this.selectedFile;
      } else {
        payload.content = this.content;
      }

      try {
        await this.ragAddDocument(payload);
        this.content = "";
        this.selectedFile = null;
        if (this.$refs.fileInput) this.$refs.fileInput.value = null;
        await this.loadDocuments();
      } catch (error) {
        console.error("Error adding document:", error);
        // Could add error notification here
      }
    },

    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
      }
    },

    triggerFileUpload() {
      this.$refs.fileInput.click();
    },

    async handleSearch() {
      if (!this.searchQuery) {
        this.searchResults = [];
        return;
      }

      try {
        const results = await this.ragSearchDocuments({
          query: this.searchQuery,
        });
        this.searchResults = results;
      } catch (error) {
        console.error("Error searching documents:", error);
        // Could add error notification here
      }
    },

    confirmDelete(docId) {
      this.deleteConfirmDocId = docId;
    },

    async proceedWithDelete() {
      if (!this.deleteConfirmDocId) return;

      try {
        await this.ragDeleteDocument(this.deleteConfirmDocId);
        // If we're in search results, refresh those too
        if (this.searchQuery && this.searchResults.length) {
          await this.handleSearch();
        }
        await this.loadDocuments();
        this.deleteConfirmDocId = null;
      } catch (error) {
        console.error("Error deleting document:", error);
        // Could add error notification here
      }
    },

    async loadDocuments() {
      try {
        await this.ragGetDocuments();
      } catch (error) {
        console.error("Error loading documents:", error);
        // Could add error notification here
      }
    },

    formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    },

    // Toggle expanded state for a document
    toggleExpand(docId) {
      this.$set(this.expandedDocs, docId, !this.expandedDocs[docId]);
    },

    // Format metadata for display
    formatMetadata(metadata) {
      if (!metadata) return "";

      // If metadata is a string, try to parse it as JSON
      let metadataObj = metadata;
      if (typeof metadata === "string") {
        try {
          metadataObj = JSON.parse(metadata);
        } catch (e) {
          return metadata; // Return as-is if not valid JSON
        }
      }

      // Format as pretty JSON
      return JSON.stringify(metadataObj, null, 2);
    },

    // Get document title from metadata or shorten doc_id if not available
    getDocTitle(doc) {
      // Try to get title from metadata
      const title = this.getDocMetadata(doc, "title");
      if (title) return title;

      // Fall back to shortened doc_id
      return this.shortenDocId(doc.doc_id);
    },

    // Extract a specific metadata field from a document
    getDocMetadata(doc, field) {
      if (!doc.metadata) return null;

      // If metadata is a string, try to parse it as JSON
      let metadata = doc.metadata;
      if (typeof metadata === "string") {
        try {
          metadata = JSON.parse(metadata);
        } catch (e) {
          return null;
        }
      }

      return metadata[field] || null;
    },

    // Determine document source type from metadata or content
    getDocSourceType(doc) {
      const source = this.getDocMetadata(doc, "source");
      if (source) {
        if (source.startsWith("http")) return "url";
        if (source.includes(".")) return "file";
      }
      return "text";
    },

    // Shorten document ID for display
    shortenDocId(docId) {
      if (!docId) return "";
      if (docId.length <= 12) return docId;

      return docId.substring(0, 6) + "..." + docId.substring(docId.length - 6);
    },

    // Format URL for display
    formatUrl(url) {
      if (!url) return "";

      try {
        const urlObj = new URL(url);
        let displayUrl = urlObj.hostname;

        // Add path if it's not just '/' and truncate if too long
        if (urlObj.pathname && urlObj.pathname !== "/") {
          const pathParts = urlObj.pathname.split("/");
          const shortenedPath =
            pathParts.length > 2 ? `/${pathParts[1]}/...` : urlObj.pathname;
          displayUrl += shortenedPath;
        }

        return displayUrl;
      } catch (e) {
        // If URL parsing fails, return truncated original
        return url.length > 30 ? url.substring(0, 27) + "..." : url;
      }
    },
  },
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #d1d5db transparent;
}
.dark .custom-scrollbar {
  scrollbar-color: #4b5563 transparent;
}

.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 2px;
}
</style>
